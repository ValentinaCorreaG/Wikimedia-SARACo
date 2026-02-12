from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from calendar import monthrange
from .models import Evento
from .forms import EventoForm

def home(request):
    return render(request, 'home.html')

def calendario_vista(request):
    """Vista principal del calendario"""
    # Obtener mes y año actual o de los parámetros
    hoy = datetime.now()
    mes = int(request.GET.get('mes', hoy.month))
    anio = int(request.GET.get('anio', hoy.year))
    
    # Calcular fechas del mes
    primer_dia = datetime(anio, mes, 1)
    ultimo_dia = datetime(anio, mes, monthrange(anio, mes)[1])
    
    # Obtener eventos del mes
    eventos = Evento.objects.filter(
        Q(fecha_inicio__year=anio, fecha_inicio__month=mes) |
        Q(fecha_fin__year=anio, fecha_fin__month=mes) |
        Q(fecha_inicio__lt=primer_dia, fecha_fin__gt=ultimo_dia)
    )
    
    # Calcular navegación
    mes_anterior = mes - 1 if mes > 1 else 12
    anio_anterior = anio if mes > 1 else anio - 1
    mes_siguiente = mes + 1 if mes < 12 else 1
    anio_siguiente = anio if mes < 12 else anio + 1
    
    # Crear estructura del calendario
    dias_semana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    # Primer día de la semana (0 = lunes, 6 = domingo)
    primer_dia_semana = primer_dia.weekday()
    
    # Crear matriz del calendario
    semanas = []
    dia_actual = 1
    total_dias = monthrange(anio, mes)[1]
    
    for semana in range(6):  # Máximo 6 semanas en un mes
        dias = []
        for dia_semana in range(7):
            if semana == 0 and dia_semana < primer_dia_semana:
                dias.append(None)
            elif dia_actual > total_dias:
                dias.append(None)
            else:
                # Buscar eventos para este día
                fecha_dia = datetime(anio, mes, dia_actual)
                eventos_dia = [e for e in eventos if e.fecha_inicio <= fecha_dia.date() <= e.fecha_fin]
                
                dias.append({
                    'numero': dia_actual,
                    'eventos': eventos_dia,
                    'es_hoy': (dia_actual == hoy.day and mes == hoy.month and anio == hoy.year)
                })
                dia_actual += 1
        
        # Solo agregar la semana si tiene al menos un día
        if any(dias):
            semanas.append(dias)
        else:
            break
    
    contexto = {
        'mes': mes,
        'anio': anio,
        'nombre_mes': primer_dia.strftime('%B'),
        'semanas': semanas,
        'dias_semana': dias_semana,
        'mes_anterior': mes_anterior,
        'anio_anterior': anio_anterior,
        'mes_siguiente': mes_siguiente,
        'anio_siguiente': anio_siguiente,
    }
    
    return render(request, 'calendario/calendario.html', contexto)


def lista_eventos(request):
    """Vista de lista de eventos (para HTMX)"""
    eventos = Evento.objects.all().order_by('fecha_inicio')
    
    # Filtro de búsqueda
    busqueda = request.GET.get('busqueda', '')
    if busqueda:
        eventos = eventos.filter(
            Q(nombre__icontains=busqueda) |
            Q(area_responsable__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )
    
    if request.htmx:
        return render(request, 'calendario/partials/eventos_lista.html', {'eventos': eventos})
    
    return render(request, 'calendario/eventos_lista.html', {'eventos': eventos})


def crear_evento(request):
    """Crear nuevo evento"""
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save()
            messages.success(request, f'Evento "{evento.nombre}" creado exitosamente.')
            
            if request.htmx:
                # IMPORTANTE: Cambiar el target y agregar trigger
                response = HttpResponse(status=204)  # ← CAMBIAR ESTA LÍNEA
                response['HX-Trigger'] = 'eventoCerrado'
                return response
            
            return redirect('lista_eventos')
        
    else:
        form = EventoForm()
    
    if request.htmx:
        return render(request, 'calendario/partials/evento_form.html', {
            'form': form,
            'titulo': 'Crear Evento',
            'accion': 'crear'
        })
    
    return render(request, 'calendario/evento_form.html', {'form': form, 'titulo': 'Crear Evento'})


def editar_evento(request, pk):
    """Editar evento existente"""
    evento = get_object_or_404(Evento, pk=pk)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            evento = form.save()
            messages.success(request, f'Evento "{evento.nombre}" actualizado exitosamente.')
            
            if request.htmx:
                eventos = Evento.objects.all().order_by('fecha_inicio')
                response = render(request, 'calendario/partials/eventos_lista.html', {'eventos': eventos})
                response['HX-Trigger'] = 'eventoCerrado'
                return response
            
            return redirect('lista_eventos')
    else:
        form = EventoForm(instance=evento)
    
    if request.htmx:
        return render(request, 'calendario/partials/evento_form.html', {
            'form': form,
            'evento': evento,
            'titulo': 'Editar Evento',
            'accion': 'editar'
        })
    
    return render(request, 'calendario/evento_form.html', {'form': form, 'evento': evento, 'titulo': 'Editar Evento'})


def eliminar_evento(request, pk):
    """Eliminar evento"""
    evento = get_object_or_404(Evento, pk=pk)
    
    if request.method == 'POST':
        nombre_evento = evento.nombre
        evento.delete()
        messages.success(request, f'Evento "{nombre_evento}" eliminado exitosamente.')
        
        if request.htmx:
            eventos = Evento.objects.all().order_by('fecha_inicio')
            response = render(request, 'calendario/partials/eventos_lista.html', {'eventos': eventos})
            response['HX-Trigger'] = 'eventoCerrado'
            return response
        
        return redirect('lista_eventos')
    
    if request.htmx:
        return render(request, 'calendario/partials/evento_eliminar.html', {'evento': evento})
    
    return render(request, 'calendario/evento_eliminar.html', {'evento': evento})


def detalle_evento(request, pk):
    """Ver detalle de un evento"""
    evento = get_object_or_404(Evento, pk=pk)
    
    if request.htmx:
        return render(request, 'calendario/partials/evento_detalle.html', {'evento': evento})
    
    return render(request, 'calendario/evento_detalle.html', {'evento': evento})