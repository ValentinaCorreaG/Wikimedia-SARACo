from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calendario/', views.calendario_vista, name='calendario'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/crear/', views.crear_evento, name='crear_evento'),
    path('eventos/<int:pk>/', views.detalle_evento, name='detalle_evento'),
    path('eventos/<int:pk>/editar/', views.editar_evento, name='editar_evento'),
    path('eventos/<int:pk>/eliminar/', views.eliminar_evento, name='eliminar_evento'),
]
