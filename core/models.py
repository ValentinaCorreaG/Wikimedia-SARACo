"""
Core app models.

Defines the Event model used for the calendar and event management.
"""
from django.db import models
from django.core.validators import MinValueValidator


class Event(models.Model):
    """
    Calendar event with start/end dates, responsible area, and expected participants.
    """
    name = models.CharField(max_length=200, verbose_name="Nombre del evento")
    start_date = models.DateField(verbose_name="Fecha de inicio")
    end_date = models.DateField(verbose_name="Fecha de fin")
    responsible_area = models.CharField(max_length=100, verbose_name="Área responsable")
    expected_participants = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Participantes esperados"
    )
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['start_date']

    def __str__(self):
        return f"{self.name} - {self.start_date.strftime('%d/%m/%Y')}"

    @property
    def duration_days(self):
        """Return the event duration in days (inclusive of start and end date)."""
        return (self.end_date - self.start_date).days + 1
