from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'responsible_area', 'expected_participants']
    list_filter = ['start_date']
    search_fields = ['name', 'responsible_area', 'description']
