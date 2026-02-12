from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'area_responsable', 'participantes_esperados', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent',
                'placeholder': 'Ej: Reunión mensual'
            }),
            'fecha_inicio': forms.DateInput(attrs={  # ← Cambiar de DateTimeInput a DateInput
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent'
            }),
            'fecha_fin': forms.DateInput(attrs={  # ← Cambiar de DateTimeInput a DateInput
                'type': 'date',  
                'class': 'w-full px-4 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent'
            }),
            
            'area_responsable': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent',
                'placeholder': 'Ej: Comunicaciones'
            }),
            'participantes_esperados': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent',
                'min': '1',
                'placeholder': 'Número de participantes'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-300 focus:border-transparent',
                'rows': 4,
                'placeholder': 'Descripción del evento (opcional)'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise forms.ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')

        return cleaned_data