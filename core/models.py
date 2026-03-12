"""
Core app models.

Defines the Event model used for the calendar and event management.
"""
from django.db import models
from django.core.validators import MinValueValidator
class Project(models.Model):
    """
    Strategic project that groups events and activities.
    """
    PROGRAM_CHOICES = [
        ('ASC', 'Apropiación social de conocimiento'),
        ('TC', 'Tecnologías y comunidades'),
    ]

    STATUS_CHOICES = [
        ('planning', 'Planeación'),
        ('active', 'Activo'),
        ('paused', 'En pausa'),
        ('finished', 'Finalizado'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nombre del proyecto")
    program = models.CharField(max_length=3, choices=PROGRAM_CHOICES, verbose_name="Programa")
    start_date = models.DateField(verbose_name="Fecha de inicio")
    end_date = models.DateField(verbose_name="Fecha de fin")
    description = models.TextField(blank=True, verbose_name="Descripción")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    responsible = models.CharField(max_length=150, verbose_name="Responsable")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-start_date']

    def __str__(self):
        return self.name
    

class Activity(models.Model):
    """
    Activity record associated with a project, including metrics and verification links.
    Field names in Spanish, code and comments in English.
    """
    proyecto = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='activities', verbose_name="Proyecto")
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la actividad")
    fecha = models.DateField(verbose_name="Fecha de la actividad")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")

    # Métricas y links de verificación
    participantes = models.PositiveIntegerField(default=0, verbose_name="Participantes")
    participantes_verificacion = models.TextField(blank=True, verbose_name="Links o verificación de participantes")

    personas_alcanzadas = models.PositiveIntegerField(default=0, verbose_name="Personas alcanzadas indirectamente")
    personas_alcanzadas_verificacion = models.TextField(blank=True, verbose_name="Links o verificación de personas alcanzadas")

    contenidos_creados = models.PositiveIntegerField(default=0, verbose_name="Contenidos creados")
    contenidos_creados_verificacion = models.TextField(blank=True, verbose_name="Links o verificación de contenidos creados")

    recursos_educativos_abiertos = models.PositiveIntegerField(default=0, verbose_name="Recursos educativos abiertos")
    recursos_educativos_abiertos_verificacion = models.TextField(blank=True, verbose_name="Links o verificación de recursos educativos abiertos")

    productos = models.PositiveIntegerField(default=0, verbose_name="Productos")
    productos_verificacion = models.TextField(blank=True, verbose_name="Links o verificación de productos")

    instituciones_participantes = models.PositiveIntegerField(default=0, verbose_name="Instituciones participantes")
    instituciones_participantes_verificacion = models.TextField(blank=True, verbose_name="Links o verificación de instituciones participantes")

    alianzas_estrategicas = models.PositiveIntegerField(default=0, verbose_name="Alianzas estratégicas")
    alianzas_estrategicas_verificacion = models.TextField(blank=True, verbose_name="Links o verificación de alianzas estratégicas")

    historias = models.PositiveIntegerField(default=0, verbose_name="Historias sobre soluciones y desafíos")
    historias_verificacion = models.TextField(blank=True, verbose_name="Links o verificación de historias")

    sostenibilidad = models.PositiveIntegerField(default=0, verbose_name="Sostenibilidad")
    sostenibilidad_verificacion = models.TextField(blank=True, verbose_name="Links o verificación de sostenibilidad")

    numero_editores = models.PositiveIntegerField(default=0, verbose_name="Número total de editores")
    numero_editores_verificacion = models.TextField(blank=True, verbose_name="Links o verificación de editores")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.nombre} ({self.fecha})"

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
