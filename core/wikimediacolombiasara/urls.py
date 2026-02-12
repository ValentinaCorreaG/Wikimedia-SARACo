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
from ...wikimediacolombiasara import views

urlpatterns = [
    # Calendario
    path('calendario/', views.calendario_vista, name='calendario'),
    
    # Eventos - Lista
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    
    # Eventos - CRUD
    path('eventos/crear/', views.crear_evento, name='crear_evento'),
    path('eventos/<int:pk>/', views.detalle_evento, name='detalle_evento'),
    path('eventos/<int:pk>/editar/', views.editar_evento, name='editar_evento'),
    path('eventos/<int:pk>/eliminar/', views.eliminar_evento, name='eliminar_evento'),
]
