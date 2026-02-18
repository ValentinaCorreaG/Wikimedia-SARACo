"""
Core app forms.

ModelForm for Event with custom widgets and cross-field validation.
"""
from django import forms
from django.utils import timezone
from .models import Event

# Area choices and colors for consistent styling
AREA_CHOICES = [
    ('', '-- Selecciona un área --'),
    ('Apropiación social de conocimiento', 'Apropiación social de conocimiento'),
    ('tecnologías y comunidades', 'Tecnologías y comunidades'),
    ('otra', 'Otra'),
]

# Color mapping for areas (professional colors)
AREA_COLORS = {
    'Apropiación social de conocimiento': {
        'bg': 'bg-blue-100',
        'border': 'border-blue-400',
        'text': 'text-blue-900',
        'accent': '#3B82F6',  # Blue
    },
    'tecnologías y comunidades': {
        'bg': 'bg-green-100',
        'border': 'border-green-400',
        'text': 'text-green-900',
        'accent': '#10B981',  # Green
    },
    'otra': {
        'bg': 'bg-purple-100',
        'border': 'border-purple-400',
        'text': 'text-purple-900',
        'accent': '#8B5CF6',  # Purple
    },
}


class EventForm(forms.ModelForm):
    """Form for creating and editing events. Validates that end date is not before start date."""

    class Meta:
        model = Event
        fields = ['name', 'start_date', 'end_date', 'responsible_area', 'expected_participants', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-primary-200 rounded-lg focus:ring-2 focus:ring-primary-300 focus:border-transparent',
                'placeholder': 'Ej: Reunión mensual'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-primary-200 rounded-lg focus:ring-2 focus:ring-primary-300 focus:border-transparent'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-primary-200 rounded-lg focus:ring-2 focus:ring-primary-300 focus:border-transparent'
            }),
            'responsible_area': forms.Select(choices=AREA_CHOICES, attrs={
                'class': 'w-full px-4 py-2 border border-primary-200 rounded-lg focus:ring-2 focus:ring-primary-300 focus:border-transparent',
                'id': 'responsible_area'
            }),
            'expected_participants': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-primary-200 rounded-lg focus:ring-2 focus:ring-primary-300 focus:border-transparent',
                'min': '1',
                'placeholder': 'Número de participantes'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-primary-200 rounded-lg focus:ring-2 focus:ring-primary-300 focus:border-transparent',
                'rows': 4,
                'placeholder': 'Descripción del evento (opcional)'
            }),
        }

    def clean_start_date(self):
        """Reject start date in the past."""
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < timezone.now().date():
            raise forms.ValidationError('La fecha de inicio no puede ser anterior a hoy.')
        return start_date

    def clean_expected_participants(self):
        """Ensure at least one participant."""
        value = self.cleaned_data.get('expected_participants')
        if value is not None and value < 1:
            raise forms.ValidationError('Debe haber al menos 1 participante.')
        return value

    def clean(self):
        """Ensure end date is not before start date."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(
                'La fecha de fin debe ser igual o posterior a la fecha de inicio.'
            )

        return cleaned_data
