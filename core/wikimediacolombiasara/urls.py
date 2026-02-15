"""
URL configuration for wikimediacolombiasara project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from wikimediacolombiasara.views import some_view

urlpatterns = [
    path('', some_view, name='home'), 
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('core.urls')), # Incluye las URLs de la app core
]

from django.urls import path
from core import views as core_views

# Note: project root urls.py includes core.urls; these patterns use English names for consistency
urlpatterns = [
    path('calendar/', core_views.calendar_view, name='calendar'),
    path('events/', core_views.event_list, name='event_list'),
    path('events/create/', core_views.create_event, name='create_event'),
    path('events/<int:pk>/', core_views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', core_views.edit_event, name='edit_event'),
    path('events/<int:pk>/delete/', core_views.delete_event, name='delete_event'),
]
