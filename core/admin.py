from django.contrib import admin
from .models import Event, Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = [
        'nombre', 'proyecto', 'fecha', 'participantes', 'personas_alcanzadas', 'contenidos_creados',
        'recursos_educativos_abiertos', 'productos', 'instituciones_participantes',
        'alianzas_estrategicas', 'historias', 'sostenibilidad', 'numero_editores'
    ]
    list_filter = ['fecha', 'proyecto']
    search_fields = ['nombre', 'descripcion', 'proyecto__name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'proyecto', 'start_date', 'end_date', 'responsible_area', 'expected_participants']
    list_filter = ['start_date', 'proyecto', 'responsible_area']
    search_fields = ['name', 'responsible_area', 'description', 'proyecto__name']
