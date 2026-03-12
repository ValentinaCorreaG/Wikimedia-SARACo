"""
Core app models.

Defines the Event model used for the calendar and event management.
"""
import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Event(models.Model):
    """
    Calendar event with start/end dates, responsible area, and expected participants.
    """
    
    class LocationChoices(models.TextChoices):
        BOGOTA = "bogota", "Bogotá"
        ANDINA = "andina", "Región Andina"
        ORINOQUIA = "orinoquia", "Región Orinoquía"
        PACIFICO = "pacifico", "Región Pacífico"
        AMAZONIA = "amazonia", "Región Amazónica"
        CARIBE = "caribe", "Región Caribe"
        VIRTUAL = "virtual", "Virtual"

    class ActivityTypeChoices(models.TextChoices):
        WORKSHOP = "workshop", "Taller de formación"
        CONFERENCE = "conference", "Charla/Conferencia"
        COMUNITARY_EVENT = "comunity_event", "Encuentro comunitario"
        EDUCATIONAL_PROGRAM = "educational_program", "Programa educativo"
        OTHER = "other", "Otro"

    name = models.CharField(max_length=200, verbose_name="Nombre del evento")
    start_date = models.DateField(verbose_name="Fecha de inicio")
    end_date = models.DateField(verbose_name="Fecha de fin")
    responsible_area = models.CharField(max_length=100, verbose_name="Área responsable")
    expected_participants = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Participantes esperados"
    )
    attendance_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        null=True,
        verbose_name="Token de asistencia",
        help_text="Identificador único usado para registrar asistencias.",
    )

    location = models.CharField(
        max_length=150,
        choices=LocationChoices.choices,
        blank=True,
        verbose_name="Ubicación donde se realizó el evento"
    )
    activity_type = models.CharField(
        max_length=20,
        choices=ActivityTypeChoices.choices,
        blank=True,
        verbose_name="Tipo de actividad"
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


class Attendance(models.Model):
    """
    Event attendance record with basic contact info and satisfaction rating.
    """

    class DepartmentChoices(models.TextChoices):
        AMAZONAS = "amazonas", "Amazonas"
        ANTIOQUIA = "antioquia", "Antioquia"
        ARAUCA = "arauca", "Arauca"
        ATLANTICO = "atlantico", "Atlántico"
        BOLIVAR = "bolivar", "Bolívar"
        BOYACA = "boyaca", "Boyacá"
        CALDAS = "caldas", "Caldas"
        CAQUETA = "caqueta", "Caquetá"
        CASANARE = "casanare", "Casanare"
        CAUCA = "cauca", "Cauca"
        CESAR = "cesar", "Cesar"
        CHOCO = "choco", "Chocó"
        CORDOBA = "cordoba", "Córdoba"
        CUNDINAMARCA = "cundinamarca", "Cundinamarca"
        DISTINTO_BOGOTA = "bogota", "Distrito Capital (Bogotá)"
        GUAINIA = "guainia", "Guainía"
        GUAVIARE = "guaviare", "Guaviare"
        HUILA = "huila", "Huila"
        LA_GUAJIRA = "laguajira", "La Guajira"
        MAGDALENA = "magdalena", "Magdalena"
        META = "meta", "Meta"
        NARINO = "narino", "Nariño"
        NORTE_SANTANDER = "nortesantander", "Norte de Santander"
        PUTUMAYO = "putumayo", "Putumayo"
        QUINDIO = "quindio", "Quindío"
        RISARALDA = "risaralda", "Risaralda"
        SANTANDER = "santander", "Santander"
        SUCRE = "sucre", "Sucre"
        TOLIMA = "tolima", "Tolima"
        VALLE = "valle", "Valle del Cauca"
        VAUPES = "vaupes", "Vaupés"
        VICHADA = "vichada", "Vichada"

    class AttendanceModeChoices(models.TextChoices):
        PRESENTIAL = "presential", "Presencial"
        VIRTUAL = "virtual", "Virtual"

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="attendances",
        verbose_name="Evento",
    )
    name = models.CharField(max_length=150, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo electrónico")
    wiki_username = models.CharField(max_length=150, blank=True, verbose_name="Usuario de Wikipedia")
    department = models.CharField(max_length=150, blank=True, choices=DepartmentChoices.choices, verbose_name="Departamento al que pertenece")
    attendance_mode = models.CharField(
        max_length=20,
        choices=AttendanceModeChoices.choices,
        verbose_name="Modo de asistencia"
    )
    satisfaction = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Satisfacción (1-5)",
        help_text="Indique su nivel de satisfacción en una escala de 1 a 5.",
    )
    comments = models.TextField(blank=True, verbose_name="Comentarios")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.event.name}"
