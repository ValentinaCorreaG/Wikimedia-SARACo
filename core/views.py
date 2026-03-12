"""
Core app views.

Handles the calendar view, event list, and CRUD operations for events.
Supports both full-page and HTMX partial responses.
"""
import json
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from calendar import monthrange
from .models import Event
from .forms import EventForm
from .forms import AttendanceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse

def base(request):
    """Render the home page."""
    return render(request, 'base.html')


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

    events = Event.objects.filter(
        Q(start_date__year=year, start_date__month=month) |
        Q(end_date__year=year, end_date__month=month) |
        Q(start_date__lt=first_day, end_date__gt=last_day)
    )

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    week_days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
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
    Event list view. Supports search via GET param 'busqueda' and area filter.
    Returns a partial template when requested via HTMX, full page otherwise.
    """
    from .forms import AREA_CHOICES
    
    events = Event.objects.all().order_by('start_date')
    search = request.GET.get('busqueda', '')
    area_filter = request.GET.get('area', '')
    
    if search:
        events = events.filter(
            Q(name__icontains=search) |
            Q(responsible_area__icontains=search) |
            Q(description__icontains=search)
        )
    
    if area_filter:
        events = events.filter(responsible_area=area_filter)

    if request.htmx:
        return render(request, 'calendar/partials/event_list.html', {'events': events})
    return render(request, 'calendar/event_list.html', {'events': events, 'area_choices': AREA_CHOICES})

@login_required
def create_event(request):
    """Create a new event. On success, redirects to event list or returns HTMX trigger."""
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


@login_required
def edit_event(request, pk):
    """Edit an existing event by primary key. Supports full page and HTMX."""
    event = get_object_or_404(Event, pk=pk)
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to create events.")

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Evento "{event.name}" actualizado exitosamente.')

            if request.htmx:
                events = Event.objects.all().order_by('start_date')
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


def delete_event(request, pk):
    """Delete an event after confirmation. Returns event list partial for HTMX or redirect."""
    event = get_object_or_404(Event, pk=pk)

    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to create events.")

    if request.method == 'POST':
        event_name = event.name
        event.delete()
        messages.success(request, f'Evento "{event_name}" eliminado exitosamente.')

        if request.htmx:
            events = Event.objects.all().order_by('start_date')
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
    event = get_object_or_404(Event, pk=pk)
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
