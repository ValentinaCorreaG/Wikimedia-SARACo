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
    """Formulario para crear y editar actividades, con etiquetas en español y campos en inglés."""
    class Meta:
        model = Activity
        fields = [
            'project', 'name', 'date', 'description', 'area',
            'participants', 'participants_verification',
            'reached_people', 'reached_people_verification',
            'created_content', 'created_content_verification',
            'open_educational_resources', 'open_educational_resources_verification',
            'products', 'products_verification',
            'participating_institutions', 'participating_institutions_verification',
            'strategic_partnerships', 'strategic_partnerships_verification',
            'stories', 'stories_verification',
            'sustainability', 'sustainability_verification',
            'editor_count', 'editor_count_verification',
        ]
        labels = {
            'project': 'Proyecto',
            'name': 'Nombre de la actividad',
            'date': 'Fecha de la actividad',
            'description': 'Descripción',
            'area': 'Área de la actividad',
            'participants': 'Participantes',
            'participants_verification': 'Links o verificación de participantes',
            'reached_people': 'Personas alcanzadas indirectamente',
            'reached_people_verification': 'Links o verificación de personas alcanzadas',
            'created_content': 'Contenidos creados',
            'created_content_verification': 'Links o verificación de contenidos creados',
            'open_educational_resources': 'Recursos educativos abiertos',
            'open_educational_resources_verification': 'Links o verificación de recursos educativos',
            'products': 'Productos',
            'products_verification': 'Links o verificación de productos',
            'participating_institutions': 'Instituciones participantes',
            'participating_institutions_verification': 'Links o verificación de instituciones participantes',
            'strategic_partnerships': 'Alianzas estratégicas',
            'strategic_partnerships_verification': 'Links o verificación de alianzas estratégicas',
            'stories': 'Historias sobre soluciones y desafíos',
            'stories_verification': 'Links o verificación de historias',
            'sustainability': 'Sostenibilidad',
            'sustainability_verification': 'Links o verificación de sostenibilidad',
            'editor_count': 'Número total de editores',
            'editor_count_verification': 'Links o verificación de editores',
        }
        widgets = {
            'project': forms.Select(attrs={'class': BASE_INPUT_CLASS}),
            'name': forms.TextInput(attrs={'class': BASE_INPUT_CLASS, 'placeholder': 'Nombre de la actividad'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': BASE_INPUT_CLASS}),
            'description': forms.Textarea(attrs={'class': BASE_INPUT_CLASS, 'rows': 4}),
            'participants': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS, 'min': '0'}),
            'participants_verification': forms.Textarea(attrs={'class': BASE_INPUT_CLASS, 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'reached_people': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS, 'min': '0'}),
            'reached_people_verification': forms.Textarea(attrs={'class': BASE_INPUT_CLASS, 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'created_content': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS, 'min': '0'}),
            'created_content_verification': forms.Textarea(attrs={'class': BASE_INPUT_CLASS, 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'open_educational_resources': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS, 'min': '0'}),
            'open_educational_resources_verification': forms.Textarea(attrs={'class': BASE_INPUT_CLASS, 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'products': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS, 'min': '0'}),
            'products_verification': forms.Textarea(attrs={'class': BASE_INPUT_CLASS, 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'participating_institutions': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS, 'min': '0'}),
            'participating_institutions_verification': forms.Textarea(attrs={'class': BASE_INPUT_CLASS, 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'strategic_partnerships': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS, 'min': '0'}),
            'strategic_partnerships_verification': forms.Textarea(attrs={'class': BASE_INPUT_CLASS, 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'stories': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS, 'min': '0'}),
            'stories_verification': forms.Textarea(attrs={'class': BASE_INPUT_CLASS, 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'sustainability': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS, 'min': '0'}),
            'sustainability_verification': forms.Textarea(attrs={'class': BASE_INPUT_CLASS, 'placeholder': 'Links o notas de verificación', 'rows': 4}),
            'editor_count': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS, 'min': '0'}),
            'editor_count_verification': forms.Textarea(attrs={'class': BASE_INPUT_CLASS, 'placeholder': 'Links o notas de verificación', 'rows': 4}),
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
        fields = ['proyecto', 'name', 'start_date', 'end_date', 'responsible_area', 'activity_type', 'location', 'expected_participants', 'description']
        widgets = {
            'proyecto': forms.Select(attrs={
                'class': BASE_INPUT_CLASS,
            }),
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
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Nombre del proyecto'
            }),
            'program': forms.Select(attrs={
                'class': BASE_INPUT_CLASS
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': BASE_INPUT_CLASS
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': BASE_INPUT_CLASS
            }),
            'status': forms.Select(attrs={
                'class': BASE_INPUT_CLASS
            }),
            'responsible': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASS,
                'placeholder': 'Responsable del proyecto'
            }),
            'description': forms.Textarea(attrs={
                'class': BASE_INPUT_CLASS,
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
