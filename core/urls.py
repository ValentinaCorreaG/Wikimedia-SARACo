from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('events/<uuid:attendance_token>/attendance/', views.register_attendance, name='register_attendance'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.edit_project, name='project_edit'),
    path('projects/<int:pk>/delete/', views.delete_project, name='project_delete'),

    # Activities CRUD
    path('activities/', views.activity_list, name='activity_list'),
    path('activities/create/', views.create_activity, name='create_activity'),
    path('activities/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('activities/<int:pk>/edit/', views.edit_activity, name='edit_activity'),
    path('activities/<int:pk>/delete/', views.delete_activity, name='delete_activity'),
]
