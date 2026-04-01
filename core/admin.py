from django.contrib import admin
from .models import Event, Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'project', 'date', 'participants', 'reached_people', 'created_content',
        'open_educational_resources', 'products', 'participating_institutions',
        'strategic_partnerships', 'stories', 'sustainability', 'editor_count'
    ]
    list_filter = ['date', 'project']
    search_fields = ['name', 'description', 'project__name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'proyecto', 'start_date', 'end_date', 'responsible_area', 'expected_participants']
    list_filter = ['start_date', 'proyecto', 'responsible_area']
    search_fields = ['name', 'responsible_area', 'description', 'proyecto__name']
