"""
Core app forms.

ModelForm for Event with custom widgets and cross-field validation.
"""
from django import forms
from django.utils import timezone
from .models import Event


class EventForm(forms.ModelForm):
    """Form for creating and editing events. Validates that end date is not before start date."""

    class Meta:
        model = Event
        fields = ['name', 'start_date', 'end_date', 'responsible_area', 'expected_participants', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent',
                'placeholder': 'Ej: Reunión mensual'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent'
            }),
            'responsible_area': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent',
                'placeholder': 'Ej: Comunicaciones'
            }),
            'expected_participants': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent',
                'min': '1',
                'placeholder': 'Número de participantes'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent',
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
