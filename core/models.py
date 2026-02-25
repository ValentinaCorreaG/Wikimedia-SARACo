"""
Core app models.

Defines the Event model used for the calendar and event management.
"""
from django.db import models
from django.utils import timezone
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

class OutreachStatsCache(models.Model):
    """Cache para las estadísticas de Outreach Dashboard"""
    campaign_slug = models.CharField(max_length=100, unique=True, default='wikimedia_colombia_2025')
    
    # Estadísticas
    programs = models.IntegerField(default=0)
    editors = models.IntegerField(default=0)
    words_added = models.BigIntegerField(default=0)
    references_added = models.IntegerField(default=0)
    article_views = models.BigIntegerField(default=0)
    articles_edited = models.IntegerField(default=0)
    articles_created = models.IntegerField(default=0)
    commons_uploads = models.IntegerField(default=0)
    
    # Metadata
    last_updated = models.DateTimeField(auto_now=True)
    is_error = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Caché de Estadísticas Outreach"
        verbose_name_plural = "Cachés de Estadísticas Outreach"
    
    def __str__(self):
        return f"Stats for {self.campaign_slug} - {self.last_updated}"
