"""
Core app views.

Handles the calendar view, event list, and CRUD operations for events.
Supports both full-page and HTMX partial responses.
"""
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime, timedelta
from calendar import monthrange
from django.contrib import messages
from django.contrib.auth import login
from .forms import EventForm, AttendanceForm, ProjectForm, ActivityForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .services import OutreachMetricsService
from .models import Event, Project, Activity
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
    activities = Activity.objects.select_related('proyecto').all().order_by('-fecha')
    projects = Project.objects.all().order_by('name')
    search = request.GET.get('busqueda', '')
    project_filter = request.GET.get('proyecto', '')
    
    if search:
        activities = activities.filter(
            Q(nombre__icontains=search) |
            Q(descripcion__icontains=search)
        )
    
    if project_filter:
        activities = activities.filter(proyecto_id=project_filter)
    
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
            messages.success(request, f'Actividad "{activity.nombre}" creada exitosamente.')
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
            messages.success(request, f'Actividad "{activity.nombre}" actualizada exitosamente.')
            if request.htmx:
                activities = Activity.objects.select_related('proyecto').all().order_by('-fecha')
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
        activity_name = activity.nombre
        activity.delete()
        messages.success(request, f'Actividad "{activity_name}" eliminada exitosamente.')
        if request.htmx:
            activities = Activity.objects.select_related('proyecto').all().order_by('-fecha')
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

    context = {
        "outreach_metrics": outreach_metrics,
        "activities_count": activities_count,
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


def register_attendance(request, attendance_token):
    """
    Register attendance to an event using its public attendance token.
    """
    event = get_object_or_404(Event, attendance_token=attendance_token)

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.event = event
            attendance.save()
            messages.success(request, '¡Gracias por registrar tu asistencia!')
            return redirect('register_attendance', attendance_token=attendance_token)
    else:
        form = AttendanceForm()

    return render(request, 'attendance/attendance_form.html', {
        'event': event,
        'form': form,
    })


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
                'nombre': activity.nombre,
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
        activities = Activity.objects.select_related('proyecto').all().order_by('-fecha')
        if search:
            activities = activities.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
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