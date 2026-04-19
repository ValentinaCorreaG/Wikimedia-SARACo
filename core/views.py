"""
Core app views.

Handles the calendar view, event list, and CRUD operations for events.
Supports both full-page and HTMX partial responses.
"""
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.db.models import Q
from datetime import datetime, timedelta
from calendar import monthrange
from django.contrib import messages
from django.contrib.auth import login
from .forms import (
    EventForm,
    AttendanceForm,
    ATTENDANCE_WIZARD_STEP_FORMS,
    ATTENDANCE_SATISFACTION_FIELD_NAMES,
    ProjectForm,
    ActivityForm,
)
from django.urls import reverse
from .services import OutreachMetricsService
from .models import Event, Project, Activity, Attendance
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist

from .reports_generator.factory import ReportGeneratorFactory
from .decorators import (
    require_create_permission,
    require_edit_permission,
    require_delete_permission,
    require_authenticated,
)

# -------------------------
# ACTIVITY VIEWS (CRUD)
# -------------------------
def activity_list(request):
    """List all activities with search and project filter support."""
    activities = Activity.objects.select_related('project').all().order_by('-date')
    projects = Project.objects.all().order_by('name')
    search = request.GET.get('busqueda', '')
    project_filter = request.GET.get('proyecto', '')
    
    if search:
        activities = activities.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    if project_filter:
        activities = activities.filter(project_id=project_filter)
    
    if request.htmx:
        return render(request, 'activities/partials/activity_list.html', {'activities': activities})
    return render(request, 'activities/activity_list.html', {'activities': activities, 'projects': projects})

def activity_detail(request, pk):
    """Show a single activity's details."""
    activity = get_object_or_404(Activity, pk=pk)
    return render(request, 'activities/partials/activity_detail.html', {'activity': activity})

@require_create_permission
def create_activity(request):
    """Create a new activity. Only superusers can create."""
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save()
            messages.success(request, f'Actividad "{activity.name}" creada exitosamente.')
            if request.htmx:
                response = HttpResponse(status=204)
                response['HX-Trigger'] = json.dumps({
                    'modalClose': {
                        'modalId': 'modal-container',
                        'contentId': 'modal-box-content',
                        'reload': True
                    }
                })
                return response
            return redirect('activity_list')
    else:
        form = ActivityForm()
    if request.htmx:
        return render(request, 'activities/partials/activity_form.html', {
            'form': form,
            'title': 'Crear Actividad',
            'action': 'crear',
            'form_action': reverse('create_activity'),
        })
    return render(request, 'activities/partials/activity_form.html', {
        'form': form,
        'title': 'Crear Actividad',
        'form_action': reverse('create_activity'),
    })

@require_edit_permission
def edit_activity(request, pk):
    """Edit an existing activity. Only superusers can edit."""
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            activity = form.save()
            messages.success(request, f'Actividad "{activity.name}" actualizada exitosamente.')
            if request.htmx:
                activities = Activity.objects.select_related('project').all().order_by('-date')
                response = render(request, 'activities/partials/activity_list.html', {'activities': activities})
                response['HX-Trigger'] = json.dumps({
                    'modalClose': {
                        'modalId': 'modal-container',
                        'contentId': 'modal-box-content',
                        'reload': True
                    }
                })
                return response
            return redirect('activity_list')
    else:
        form = ActivityForm(instance=activity)
    if request.htmx:
        return render(request, 'activities/partials/activity_form.html', {
            'form': form,
            'activity': activity,
            'title': 'Editar Actividad',
            'action': 'editar',
            'form_action': reverse('edit_activity', args=[activity.pk]),
        })
    return render(request, 'activities/partials/activity_form.html', {
        'form': form,
        'activity': activity,
        'title': 'Editar Actividad',
        'form_action': reverse('edit_activity', args=[activity.pk]),
    })

@require_delete_permission
def delete_activity(request, pk):
    """Delete an activity. Only superusers can delete."""
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        activity_name = activity.name
        activity.delete()
        messages.success(request, f'Actividad "{activity_name}" eliminada exitosamente.')
        if request.htmx:
            activities = Activity.objects.select_related('project').all().order_by('-date')
            response = render(request, 'activities/partials/activity_list.html', {'activities': activities})
            response['HX-Trigger'] = json.dumps({
                'modalClose': {
                    'modalId': 'modal-container',
                    'contentId': 'modal-box-content',
                    'reload': True
                }
            })
            return response
        return redirect('activity_list')
    if request.htmx:
        return render(request, 'activities/partials/activity_delete.html', {'activity': activity})
    return render(request, 'activities/partials/activity_delete.html', {'activity': activity})


def base(request):
    """Render the home page."""
    outreach_metrics = OutreachMetricsService().fetch_metrics()
    activities_count = Event.objects.count()
    
    # Calcular departamentos únicos alcanzados en proyectos
    unique_departments_count = Attendance.objects.filter(
        event__proyecto__isnull=False
    ).exclude(
        department=''
    ).values_list('department', flat=True).distinct().count()

    context = {
        "outreach_metrics": outreach_metrics,
        "activities_count": activities_count,
        "unique_departments_count": unique_departments_count,
        "active_programs": 2,
    }

    return render(request, 'base.html', context)

def calendar_view(request):
    """
    Main calendar view. Renders a month grid with events.
    Month and year come from GET params (mes, anio) or default to current date.
    """
    today = datetime.now()
    month = int(request.GET.get('mes', today.month))
    year = int(request.GET.get('anio', today.year))

    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, monthrange(year, month)[1])

    events = Event.objects.select_related('proyecto').filter(
        Q(start_date__year=year, start_date__month=month) |
        Q(end_date__year=year, end_date__month=month) |
        Q(start_date__lt=first_day, end_date__gt=last_day)
    )

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    week_days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']

    # -------------------------
    # ACTIVITY VIEWS (CRUD)
    # -------------------------
    first_weekday = first_day.weekday()

    weeks = []
    current_day = 1
    total_days = monthrange(year, month)[1]

    for week in range(6):
        days = []
        for weekday in range(7):
            if week == 0 and weekday < first_weekday:
                days.append(None)
            elif current_day > total_days:
                days.append(None)
            else:
                day_date = datetime(year, month, current_day)
                day_events = [e for e in events if e.start_date <= day_date.date() <= e.end_date]
                days.append({
                    'day_number': current_day,
                    'events': day_events,
                    'is_today': (current_day == today.day and month == today.month and year == today.year)
                })
                current_day += 1
        if any(days):
            weeks.append(days)
        else:
            break

    context = {
        'month': month,
        'year': year,
        'month_name': first_day.strftime('%B'),
        'weeks': weeks,
        'week_days': week_days,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'calendar/calendar.html', context)


def event_list(request):
    """
    Event list view. Supports search via GET param 'busqueda' and project filter.
    Returns a partial template when requested via HTMX, full page otherwise.
    """
    events = Event.objects.select_related('proyecto').all().order_by('start_date')
    projects = Project.objects.all().order_by('name')
    search = request.GET.get('busqueda', '')
    project_filter = request.GET.get('proyecto', '')
    
    if search:
        events = events.filter(
            Q(name__icontains=search) |
            Q(responsible_area__icontains=search) |
            Q(description__icontains=search)
        )
    
    if project_filter:
        events = events.filter(proyecto_id=project_filter)

    if request.htmx:
        return render(request, 'calendar/partials/event_list.html', {'events': events})
    return render(request, 'calendar/event_list.html', {'events': events, 'projects': projects})

@require_create_permission
def create_event(request):
    """Create a new event. Only superusers can create."""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Evento "{event.name}" creado exitosamente.')

            if request.htmx:
                response = HttpResponse(status=204)
                response['HX-Trigger'] = json.dumps({
                    'modalClose': {
                        'modalId': 'modal-container',
                        'contentId': 'modal-box-content',
                        'reload': True
                    }
                })
                return response
            return redirect('event_list')
    else:
        form = EventForm()

    if request.htmx:
        return render(request, 'calendar/partials/event_form.html', {
            'form': form,
            'title': 'Crear Evento',
            'action': 'crear'
        })
    return render(request, 'calendar/partials/event_form.html', {'form': form, 'title': 'Crear Evento'})


@require_edit_permission
def edit_event(request, pk):
    """Edit an existing event. Only superusers can edit."""
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Evento "{event.name}" actualizado exitosamente.')

            if request.htmx:
                events = Event.objects.select_related('proyecto').all().order_by('start_date')
                response = render(request, 'calendar/partials/event_list.html', {'events': events})
                response['HX-Trigger'] = json.dumps({
                    'modalClose': {
                        'modalId': 'modal-container',
                        'contentId': 'modal-box-content',
                        'reload': True
                    }
                })
                return response
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    if request.htmx:
        return render(request, 'calendar/partials/event_form.html', {
            'form': form,
            'event': event,
            'title': 'Editar Evento',
            'action': 'editar'
        })
    return render(request, 'calendar/partials/event_form.html', {'form': form, 'event': event, 'title': 'Editar Evento'})


@require_delete_permission
def delete_event(request, pk):
    """Delete an event. Only superusers can delete."""
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        event_name = event.name
        event.delete()
        messages.success(request, f'Evento "{event_name}" eliminado exitosamente.')

        if request.htmx:
            events = Event.objects.select_related('proyecto').all().order_by('start_date')
            response = render(request, 'calendar/partials/event_list.html', {'events': events})
            response['HX-Trigger'] = json.dumps({
                'modalClose': {
                    'modalId': 'modal-container',
                    'contentId': 'modal-box-content',
                    'reload': True
                }
            })
            return response
        return redirect('event_list')

    if request.htmx:
        return render(request, 'calendar/partials/event_delete.html', {'event': event})
    return render(request, 'calendar/partials/event_delete.html', {'event': event})


def event_detail(request, pk):
    """Show a single event's details. Renders partial for HTMX modal, full page otherwise."""
    event = get_object_or_404(Event.objects.select_related('proyecto'), pk=pk)
    attendance_path = reverse("register_attendance", args=[event.attendance_token])
    attendance_url = request.build_absolute_uri(attendance_path)

    if request.htmx:
        return render(request, 'calendar/partials/event_detail.html', {'event': event, 'attendance_url': attendance_url})
    return render(request, 'calendar/partials/event_detail.html', {'event': event, 'attendance_url': attendance_url})


ATTENDANCE_WIZARD_STEP_COUNT = len(ATTENDANCE_WIZARD_STEP_FORMS)

ATTENDANCE_WIZARD_SECTION_TITLES = (
    "Sección 1 — Tratamiento de datos e identificación",
    "Sección 2 — Datos demográficos",
    "Sección 3 — Aceptabilidad",
    "Sección 4 — Evaluación de apropiación",
    "Sección 5 — Retroalimentación",
)

ATTENDANCE_WIZARD_STEP_TITLES = (
    "Tratamiento de datos",
    "Datos demográficos",
    "Aceptabilidad",
    "Evaluación de apropiación",
    "Retroalimentación",
)


def _attendance_wizard_session_key(attendance_token):
    return f"attendance_wizard_{attendance_token}"


def _attendance_wizard_completed_key(attendance_token):
    return f"attendance_wizard_completed_{attendance_token}"


def _first_incomplete_wizard_step(data):
    """
    Return the first step (1–5) that is missing required data, or None if the
    wizard payload is complete (ready for final validation on step 5 POST).
    """
    w = data or {}
    if (
        not (w.get("name") or "").strip()
        or not (w.get("email") or "").strip()
        or w.get("accepts_data_processing") is not True
    ):
        return 1
    if not w.get("department") or not w.get("attendance_mode"):
        return 2
    for f in ATTENDANCE_SATISFACTION_FIELD_NAMES:
        if w.get(f) is None:
            return 3
    inc = w.get("activity_incidence")
    if not inc:
        return 4
    other = (w.get("activity_incidence_other") or "").strip()
    if inc == Attendance.ActivityIncidenceChoices.OTHER and not other:
        return 4
    if not (w.get("learned_new_aspect") or "").strip() or not (
        w.get("interesting_aspect_discuss") or ""
    ).strip():
        return 4
    if not w.get("future_participation"):
        return 5
    return None


def register_attendance(request, attendance_token):
    """
    Multi-step attendance registration (session-backed wizard), then thank-you page.
    """
    event = get_object_or_404(Event, attendance_token=attendance_token)
    session_key = _attendance_wizard_session_key(attendance_token)
    completed_key = _attendance_wizard_completed_key(attendance_token)
    wizard_url = reverse("register_attendance", kwargs={"attendance_token": attendance_token})

    if request.GET.get("completado") == "1":
        if not request.session.pop(completed_key, False):
            return redirect(wizard_url)
        return render(
            request,
            "attendance/attendance_thanks.html",
            {"event": event},
        )

    if request.GET.get("reiniciar") == "1":
        request.session.pop(session_key, None)
        request.session.pop(completed_key, None)
        messages.info(request, "Se reinició el formulario.")
        return redirect(wizard_url)

    session_data = request.session.get(session_key, {})

    if request.method == "POST":
        try:
            posted_step = int(request.POST.get("wizard_step", "1"))
        except (TypeError, ValueError):
            posted_step = 1
        posted_step = max(1, min(posted_step, ATTENDANCE_WIZARD_STEP_COUNT))

        form_cls = ATTENDANCE_WIZARD_STEP_FORMS[posted_step - 1]
        form = form_cls(request.POST)
        if form.is_valid():
            merged = {**session_data, **form.cleaned_data}
            request.session[session_key] = merged
            request.session.modified = True

            if posted_step < ATTENDANCE_WIZARD_STEP_COUNT:
                next_step = posted_step + 1
                return redirect(f"{wizard_url}?step={next_step}")

            final_form = AttendanceForm(data=merged)
            if final_form.is_valid():
                attendance = final_form.save(commit=False)
                attendance.event = event
                attendance.save()
                request.session.pop(session_key, None)
                request.session[completed_key] = True
                messages.success(
                    request,
                    "¡Gracias por registrar tu asistencia y completar la encuesta!",
                )
                return redirect(f"{wizard_url}?completado=1")

            messages.error(
                request,
                "No se pudo guardar el registro. Revise los datos e intente de nuevo.",
            )
            return render(
                request,
                "attendance/attendance_wizard.html",
                {
                    "event": event,
                    "form": final_form,
                    "step": ATTENDANCE_WIZARD_STEP_COUNT,
                    "total_steps": ATTENDANCE_WIZARD_STEP_COUNT,
                    "prev_step": ATTENDANCE_WIZARD_STEP_COUNT - 1,
                    "section_title": ATTENDANCE_WIZARD_SECTION_TITLES[
                        ATTENDANCE_WIZARD_STEP_COUNT - 1
                    ],
                    "step_titles": ATTENDANCE_WIZARD_STEP_TITLES,
                    "session_data": merged,
                    "show_final_validation_errors": True,
                },
            )

        return render(
            request,
            "attendance/attendance_wizard.html",
            {
                "event": event,
                "form": form,
                "step": posted_step,
                "total_steps": ATTENDANCE_WIZARD_STEP_COUNT,
                "prev_step": posted_step - 1 if posted_step > 1 else None,
                "section_title": ATTENDANCE_WIZARD_SECTION_TITLES[posted_step - 1],
                "step_titles": ATTENDANCE_WIZARD_STEP_TITLES,
                "session_data": session_data,
                "show_final_validation_errors": False,
            },
        )

    try:
        step = int(request.GET.get("step", "1"))
    except (TypeError, ValueError):
        step = 1
    step = max(1, min(step, ATTENDANCE_WIZARD_STEP_COUNT))

    first_incomplete = _first_incomplete_wizard_step(session_data)
    if first_incomplete is not None and step > first_incomplete:
        return redirect(f"{wizard_url}?step={first_incomplete}")

    form_cls = ATTENDANCE_WIZARD_STEP_FORMS[step - 1]
    form = form_cls(initial=session_data)

    return render(
        request,
        "attendance/attendance_wizard.html",
        {
            "event": event,
            "form": form,
            "step": step,
            "total_steps": ATTENDANCE_WIZARD_STEP_COUNT,
            "prev_step": step - 1 if step > 1 else None,
            "section_title": ATTENDANCE_WIZARD_SECTION_TITLES[step - 1],
            "step_titles": ATTENDANCE_WIZARD_STEP_TITLES,
            "session_data": session_data,
            "show_final_validation_errors": False,
        },
    )


# -------------------------
# PROJECT VIEWS (CRUD)
# -------------------------

def project_list(request):
    """List all projects with search support."""
    projects = Project.objects.all()
    search = request.GET.get('busqueda', '')
    
    if search:
        projects = projects.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(responsible__icontains=search)
        )

    if request.htmx:
        return render(request, 'projects/partials/project_list.html', {
            'projects': projects
        })

    return render(request, 'projects/project_list.html', {
        'projects': projects
    })

def project_detail(request, pk):
    """Show a single project's details. Renders partial for HTMX modal, full page otherwise."""
    project = get_object_or_404(Project, pk=pk)

    if request.htmx:
        return render(request, 'projects/partials/project_detail.html', {'project': project})
    return render(request, 'projects/partials/project_detail.html', {'project': project})

@require_create_permission
def project_create(request):
    """Create a new project. Only superusers can create."""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()

            if request.htmx:
                response = HttpResponse(status=204)
                response['HX-Trigger'] = json.dumps({
                    'modalClose': {
                        'modalId': 'modal-container',
                        'contentId': 'modal-box-content',
                        'reload': True
                    }
                })
                return response

            return redirect('project_list')

    else:
        form = ProjectForm()

    return render(request, 'projects/partials/project_form.html', {
        'form': form,
        'title': 'Nuevo Proyecto',
        'form_action': reverse('project_create'),
    })


@require_edit_permission
def edit_project(request, pk):
    """Edit existing project. Only superusers can edit."""
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Proyecto "{project.name}" actualizado exitosamente.')

            if request.htmx:
                response = HttpResponse(status=204)
                response['HX-Trigger'] = json.dumps({
                    'modalClose': {
                        'modalId': 'modal-container',
                        'contentId': 'modal-box-content',
                        'reload': True
                    }
                })
                return response

            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/partials/project_form.html', {
        'form': form,
        'project': project,
        'title': 'Editar Proyecto',
        'action': 'editar',
        'form_action': reverse('project_edit', args=[project.pk]),
    })


# -------------------------
# REPORTS VIEW
# -------------------------
@require_authenticated
def report_list(request):
    """
    Unified reports view aggregating Activities, Events, and Projects.
    Supports filtering by type (activities|events|projects|all) and search.
    Returns partial template for HTMX requests, full page otherwise.
    """
    # Get filter and search parameters
    report_type = request.GET.get('type', 'all')  # all, activities, events, projects
    search = request.GET.get('busqueda', '')
    
    # Initialize empty report list
    reports = []
    
    # Helper function to normalize report objects
    def add_activity_reports(activities):
        for activity in activities:
            reports.append({
                'id': activity.id,
                'nombre': activity.name,
                'project_name': activity.project.name,
                'area': activity.get_area_display() if activity.area else 'Sin especificar',
                'tipo': 'Actividad',
                'object_type': 'activity',
                'object': activity,
            })
    
    def add_event_reports(events):
        for event in events:
            reports.append({
                'id': event.id,
                'nombre': event.name,
                'area': event.responsible_area,
                'project_name': event.proyecto.name,
                'tipo': event.get_activity_type_display() or 'Evento',
                'object_type': 'event',
                'object': event,
            })
    
    def add_project_reports(projects):
        for project in projects:
            reports.append({
                'id': project.id,
                'nombre': project.name,
                'area': project.get_program_display(),
                'tipo': 'Proyecto',
                'object_type': 'project',
                'object': project,
            })
    
    # Filter by type and search
    if report_type in ['all', 'activities']:
        activities = Activity.objects.select_related('project').all().order_by('-date')
        if search:
            activities = activities.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        add_activity_reports(activities)
    
    if report_type in ['all', 'events']:
        events = Event.objects.select_related('proyecto').all().order_by('-start_date')
        if search:
            events = events.filter(
                Q(name__icontains=search) |
                Q(responsible_area__icontains=search) |
                Q(description__icontains=search)
            )
        add_event_reports(events)
    
    if report_type in ['all', 'projects']:
        projects = Project.objects.all().order_by('-start_date')
        if search:
            projects = projects.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(responsible__icontains=search)
            )
        add_project_reports(projects)
    
    # Sort all reports by nombre
    reports.sort(key=lambda x: x['nombre'].lower())
    
    context = {
        'reports': reports,
        'report_type': report_type,
        'search': search,
    }
    
    if request.htmx:
        return render(request, 'reports/partials/report_list.html', context)
    return render(request, 'reports/report_list.html', context)

@require_authenticated
@require_http_methods(["GET"])
def download_report(request, report_type, instance_id):
    """
    Unified view to download Excel report for any model type.
    
    Args:
        request: HttpRequest object
        report_type: Type of report ('activity', 'event', 'project')
        instance_id: ID of the instance to generate report for
        
    Returns:
        HttpResponse with Excel file
        
    Raises:
        Http404: If instance doesn't exist or report type is invalid
    """
    try:
        # Create the appropriate generator using the factory
        generator = ReportGeneratorFactory.create(report_type, instance_id)
        
        # Optional: Add permission checks here
        # if not request.user.has_perm('your_app.view_activity'):
        #     raise PermissionDenied("No tienes permiso para descargar este reporte")
        
        # Validate the instance
        is_valid, error_msg = generator.validate_instance()
        if not is_valid:
            raise Http404(f"Error al generar reporte: {error_msg}")
        
        # Generate the Excel file
        excel_file = generator.generate_excel()
        filename = generator.get_filename()
        
        # Create HTTP response
        response = HttpResponse(
            excel_file.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except ValueError as e:
        # Invalid report type
        raise Http404(f"Tipo de reporte inválido: {str(e)}")
        
    except ObjectDoesNotExist as e:
        # Instance not found
        raise Http404(str(e))
        
    except Exception as e:
        # Log the error in production
        # logger.error(f"Error generating report: {str(e)}", exc_info=True)
        raise Http404(f"Error al generar el reporte: {str(e)}")




@require_delete_permission
def export_report_stub(request, object_type, pk):
    """
    Stub endpoint for exporting individual reports.
    Only superusers can export reports.
    Placeholder for CSV/PDF export functionality.
    """
    # Placeholder: In future, implement actual export logic
    # For now, return a simple response or redirect
    messages.info(request, f'Export functionality coming soon for {object_type} #{pk}')
    return HttpResponse(status=204)


@require_delete_permission
def delete_project(request, pk):
    """Delete project with modal confirmation. Only superusers can delete."""
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        name = project.name
        project.delete()
        messages.success(request, f'Proyecto "{name}" eliminado exitosamente.')

        if request.htmx:
            response = HttpResponse(status=204)
            response['HX-Trigger'] = json.dumps({
                'modalClose': {
                    'modalId': 'modal-container',
                    'contentId': 'modal-box-content',
                    'reload': True
                }
            })
            return response

        return redirect('project_list')

    return render(request, 'projects/partials/project_delete.html', {
        'project': project
    })


# -------------------------
# ABOUT US VIEW
# -------------------------

def about_us(request):
    """Redirect to Wikimedia Colombia official page in Spanish."""
    return redirect('https://es.m.wikipedia.org/wiki/Wikimedia_Colombia')