from .models import Event, Project, Activity, Attendance
from django import forms
from django.utils import timezone

# Base CSS classes for form inputs
BASE_INPUT_CLASS = (
    "w-full px-4 py-2 border border-primary-200 rounded-lg "
    "focus:ring-2 focus:ring-primary-300 focus:border-transparent"
)

from .models import Event, Project

class ActivityForm(forms.ModelForm):
    """Formulario para crear y editar actividades, con etiquetas en español y campos en español."""
    class Meta:
        model = Activity
        fields = [
            'proyecto', 'nombre', 'fecha', 'descripcion',
            'participantes', 'participantes_verificacion',
            'personas_alcanzadas', 'personas_alcanzadas_verificacion',
            'contenidos_creados', 'contenidos_creados_verificacion',
            'recursos_educativos_abiertos', 'recursos_educativos_abiertos_verificacion',
            'productos', 'productos_verificacion',
            'instituciones_participantes', 'instituciones_participantes_verificacion',
            'alianzas_estrategicas', 'alianzas_estrategicas_verificacion',
            'historias', 'historias_verificacion',
            'sostenibilidad', 'sostenibilidad_verificacion',
            'numero_editores', 'numero_editores_verificacion',
        ]
        labels = {
            'proyecto': 'Proyecto',
            'nombre': 'Nombre de la actividad',
            'fecha': 'Fecha de la actividad',
            'descripcion': 'Descripción',
            'participantes': 'Participantes',
            'participantes_verificacion': 'Links o verificación de participantes',
            'personas_alcanzadas': 'Personas alcanzadas indirectamente',
            'personas_alcanzadas_verificacion': 'Links o verificación de personas alcanzadas',
            'contenidos_creados': 'Contenidos creados',
            'contenidos_creados_verificacion': 'Links o verificación de contenidos creados',
            'recursos_educativos_abiertos': 'Recursos educativos abiertos',
            'recursos_educativos_abiertos_verificacion': 'Links o verificación de recursos educativos',
            'productos': 'Productos',
            'productos_verificacion': 'Links o verificación de productos',
            'instituciones_participantes': 'Instituciones participantes',
            'instituciones_participantes_verificacion': 'Links o verificación de instituciones participantes',
            'alianzas_estrategicas': 'Alianzas estratégicas',
            'alianzas_estrategicas_verificacion': 'Links o verificación de alianzas estratégicas',
            'historias': 'Historias sobre soluciones y desafíos',
            'historias_verificacion': 'Links o verificación de historias',
            'sostenibilidad': 'Sostenibilidad',
            'sostenibilidad_verificacion': 'Links o verificación de sostenibilidad',
            'numero_editores': 'Número total de editores',
            'numero_editores_verificacion': 'Links o verificación de editores',
        }
        widgets = {
            'proyecto': forms.Select(attrs={'class': 'w-full select select-bordered'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full input input-bordered', 'placeholder': 'Nombre de la actividad'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'w-full input input-bordered'}),
            'descripcion': forms.Textarea(attrs={'class': 'w-full textarea textarea-bordered', 'rows': 4}),
            'participantes': forms.NumberInput(attrs={'class': 'w-full input input-bordered', 'min': '0'}),
            'participantes_verificacion': forms.Textarea(attrs={'class': 'w-full textarea textarea-bordered', 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'personas_alcanzadas': forms.NumberInput(attrs={'class': 'w-full input input-bordered', 'min': '0'}),
            'personas_alcanzadas_verificacion': forms.Textarea(attrs={'class': 'w-full textarea textarea-bordered', 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'contenidos_creados': forms.NumberInput(attrs={'class': 'w-full input input-bordered', 'min': '0'}),
            'contenidos_creados_verificacion': forms.Textarea(attrs={'class': 'w-full textarea textarea-bordered', 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'recursos_educativos_abiertos': forms.NumberInput(attrs={'class': 'w-full input input-bordered', 'min': '0'}),
            'recursos_educativos_abiertos_verificacion': forms.Textarea(attrs={'class': 'w-full textarea textarea-bordered', 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'productos': forms.NumberInput(attrs={'class': 'w-full input input-bordered', 'min': '0'}),
            'productos_verificacion': forms.Textarea(attrs={'class': 'w-full textarea textarea-bordered', 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'instituciones_participantes': forms.NumberInput(attrs={'class': 'w-full input input-bordered', 'min': '0'}),
            'instituciones_participantes_verificacion': forms.Textarea(attrs={'class': 'w-full textarea textarea-bordered', 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'alianzas_estrategicas': forms.NumberInput(attrs={'class': 'w-full input input-bordered', 'min': '0'}),
            'alianzas_estrategicas_verificacion': forms.Textarea(attrs={'class': 'w-full textarea textarea-bordered', 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'historias': forms.NumberInput(attrs={'class': 'w-full input input-bordered', 'min': '0'}),
            'historias_verificacion': forms.Textarea(attrs={'class': 'w-full textarea textarea-bordered', 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'sostenibilidad': forms.NumberInput(attrs={'class': 'w-full input input-bordered', 'min': '0'}),
            'sostenibilidad_verificacion': forms.Textarea(attrs={'class': 'w-full textarea textarea-bordered', 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'numero_editores': forms.NumberInput(attrs={'class': 'w-full input input-bordered', 'min': '0'}),
            'numero_editores_verificacion': forms.Textarea(attrs={'class': 'w-full textarea textarea-bordered', 'placeholder': 'Links o notas de verificación', 'rows': 4}),
        }

# Area choices and colors for consistent styling
AREA_CHOICES = [
    ('', '-- Selecciona un área --'),
    ('Apropiación social de conocimiento', 'Apropiación social de conocimiento'),
    ('tecnologías y comunidades', 'Tecnologías y comunidades'),
    ('otra', 'Otra'),
]


class EventForm(forms.ModelForm):
    """Form for creating and editing events."""

    class Meta:
        model = Event
        fields = ['name', 'start_date', 'end_date', 'responsible_area', 'activity_type', 'location', 'expected_participants', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Ej: Reunión mensual'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': BASE_INPUT_CLASS,
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': BASE_INPUT_CLASS,
            }),
            'responsible_area': forms.Select(choices=AREA_CHOICES, attrs={
                'class': BASE_INPUT_CLASS,
                'id': 'responsible_area'
            }),
            'activity_type': forms.Select(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Tipo de actividad'
            }),
            'location': forms.Select(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Ubicación de el evento'
            }),
            'expected_participants': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASS,
                'min': '1',
                'placeholder': 'Número de participantes'
            }),
            'description': forms.Textarea(attrs={
                'class': BASE_INPUT_CLASS,
                'rows': 4,
                'placeholder': 'Descripción del evento (opcional)'
            }),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < timezone.now().date():
            raise forms.ValidationError('La fecha de inicio no puede ser anterior a hoy.')
        return start_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(
                'La fecha de fin debe ser igual o posterior a la fecha de inicio.'
            )
        return cleaned_data

class ProjectForm(forms.ModelForm):
    """Form for creating and editing projects."""

    class Meta:
        model = Project
        fields = [
            'name', 'program', 'start_date',
            'end_date', 'status', 'responsible', 'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full input input-bordered',
                'placeholder': 'Nombre del proyecto'
            }),
            'program': forms.Select(attrs={
                'class': 'w-full select select-bordered'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full input input-bordered'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full input input-bordered'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full select select-bordered'
            }),
            'responsible': forms.TextInput(attrs={
                'class': 'w-full input input-bordered',
                'placeholder': 'Responsable del proyecto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full textarea textarea-bordered',
                'rows': 4
            }),
        }
        
class AttendanceForm(forms.ModelForm):
    """Form for registering attendance to an event."""

    class Meta:
        model = Attendance
        fields = ['name', 'email', 'wiki_username', 'department', 'attendance_mode', 'satisfaction', 'comments']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Tu nombre completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'tu@correo.com'
            }),
            'wiki_username': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Tu usuario de Wikipedia (opcional)'
            }),
            'department': forms.Select(attrs={
                'class': BASE_INPUT_CLASS,
            }),
            'attendance_mode': forms.Select(attrs={
                'class': BASE_INPUT_CLASS,
            }),
            'satisfaction': forms.NumberInput(attrs={
                'class': BASE_INPUT_CLASS,
                'min': '1',
                'max': '5',
                'placeholder': 'Califica de 1 a 5'
            }),
            'comments': forms.Textarea(attrs={
                'class': BASE_INPUT_CLASS,
                'rows': 4,
                'placeholder': 'Comentarios o sugerencias (opcional)'
            }),
        }
