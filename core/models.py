from django.db import models
from django.core.validators import MinValueValidator

class Evento(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del evento")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de fin")
    area_responsable = models.CharField(max_length=100, verbose_name="Área responsable")
    participantes_esperados = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Participantes esperados"
    )
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['fecha_inicio']

    def __str__(self):
        return f"{self.nombre} - {self.fecha_inicio.strftime('%d/%m/%Y')}"

    @property
    def duracion_dias(self):
        """Retorna la duración del evento en días"""
        return (self.fecha_fin - self.fecha_inicio).days + 1