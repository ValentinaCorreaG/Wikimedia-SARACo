from .models import Event, Project, Activity, Attendance
from django import forms
from django.utils import timezone

# Base CSS classes for form inputs
BASE_INPUT_CLASS = (
    "w-full px-4 py-2 border border-primary-200 rounded-lg "
    "focus:ring-2 focus:ring-primary-300 focus:border-transparent"
)

# Escala Likert 1–5 para aceptabilidad (mismas etiquetas que en la encuesta de referencia)
SATISFACTION_SCALE_CHOICES = [
    (1, "Muy insatisfecho"),
    (2, "Insatisfecho"),
    (3, "Satisfecho"),
    (4, "Muy satisfecho"),
    (5, "Completamente satisfecho"),
]


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
            'event_participation', 'event_participation_verification',
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
            'event_participation': 'Participación en eventos',
            'event_participation_verification': 'Links o verificación de participación en eventos',
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
            'event_participation': forms.NumberInput(attrs={'class': BASE_INPUT_CLASS, 'min': '0'}),
            'event_participation_verification': forms.Textarea(attrs={'class': BASE_INPUT_CLASS, 'placeholder': 'Links o notas de verificación', 'rows': 4}),
        }

# Area choices and colors for consistent styling
AREA_CHOICES = [
    ('', '-- Selecciona un área --'),
    ('Apropiación social de conocimiento', 'Apropiación social de conocimiento'),
    ('tecnologías y comunidades', 'Tecnologías y comunidades'),
    ('Dirección Administrativa', 'Dirección Administrativa'),
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
        
class AttendanceStep1Form(forms.ModelForm):
    """Sección 1: tratamiento de datos e identificación."""

    class Meta:
        model = Attendance
        fields = ("accepts_data_processing", "name", "email", "wiki_username")
        widgets = {
            "accepts_data_processing": forms.CheckboxInput(
                attrs={"class": "checkbox checkbox-primary"}
            ),
            "name": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "Tu nombre completo",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "tu@correo.com",
                }
            ),
            "wiki_username": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "Tu usuario de Wikipedia (opcional)",
                }
            ),
        }

    def clean_accepts_data_processing(self):
        value = self.cleaned_data.get("accepts_data_processing")
        if not value:
            raise forms.ValidationError(
                "Debe aceptar el tratamiento de datos personales para continuar."
            )
        return value


class AttendanceStep2Form(forms.ModelForm):
    """Sección 2: datos demográficos."""

    class Meta:
        model = Attendance
        fields = ("department", "attendance_mode")
        widgets = {
            "department": forms.Select(attrs={"class": BASE_INPUT_CLASS}),
            "attendance_mode": forms.Select(attrs={"class": BASE_INPUT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["department"].required = True


class AttendanceStep3Form(forms.ModelForm):
    """Sección 3: aceptabilidad (cinco ítems 1–5, escala Likert con radios)."""

    class Meta:
        model = Attendance
        fields = (
            "satisfaction_methodology",
            "satisfaction_session_usefulness",
            "satisfaction_schedule_timing",
            "satisfaction_logistics",
            "satisfaction_activity_usefulness",
        )
        labels = {
            "satisfaction_methodology": "La metodología usada en la sesión",
            "satisfaction_session_usefulness": "La utilidad de la sesión",
            "satisfaction_schedule_timing": "El horario del encuentro y el tiempo de la actividad",
            "satisfaction_logistics": "Organización logística de la actividad",
            "satisfaction_activity_usefulness": "Utilidad de la actividad",
        }

    @classmethod
    def apply_satisfaction_radio_fields(cls, form):
        """Sustituye los cinco enteros por TypedChoiceField + RadioSelect (mismo valor 1–5 en BD)."""
        for fname in cls.Meta.fields:
            form.fields[fname] = forms.TypedChoiceField(
                label=cls.Meta.labels[fname],
                coerce=int,
                choices=SATISFACTION_SCALE_CHOICES,
                required=True,
                widget=forms.RadioSelect(),
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_satisfaction_radio_fields(self)


class AttendanceStep4Form(forms.ModelForm):
    """Sección 4: evaluación de apropiación."""

    class Meta:
        model = Attendance
        fields = (
            "activity_incidence",
            "activity_incidence_other",
            "learned_new_aspect",
            "interesting_aspect_discuss",
        )
        widgets = {
            "activity_incidence": forms.RadioSelect,
            "activity_incidence_other": forms.Textarea(
                attrs={"class": BASE_INPUT_CLASS, "rows": 3}
            ),
            "learned_new_aspect": forms.Textarea(
                attrs={"class": BASE_INPUT_CLASS, "rows": 3}
            ),
            "interesting_aspect_discuss": forms.Textarea(
                attrs={"class": BASE_INPUT_CLASS, "rows": 3}
            ),
        }
        labels = {
            "activity_incidence": "¿Cuál fue la incidencia que tuvo la actividad?",
            "activity_incidence_other": "Especifique (opción «Otro»)",
            "learned_new_aspect": "Mencione un aspecto que no sabía antes de este taller",
            "interesting_aspect_discuss": (
                "Mencione un (1) aspecto que fue tan interesante que lo discutiría con otras personas"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["activity_incidence"].choices = Attendance.ActivityIncidenceChoices.choices
        self.fields["activity_incidence"].required = True
        self.fields["learned_new_aspect"].required = True
        self.fields["interesting_aspect_discuss"].required = True

    def clean(self):
        cleaned = super().clean()
        incidence = cleaned.get("activity_incidence")
        other = (cleaned.get("activity_incidence_other") or "").strip()
        if incidence == Attendance.ActivityIncidenceChoices.OTHER and not other:
            self.add_error(
                "activity_incidence_other",
                "Describa la incidencia cuando elige la opción «Otro».",
            )
        return cleaned


class AttendanceStep5Form(forms.ModelForm):
    """Sección 5: retroalimentación."""

    class Meta:
        model = Attendance
        fields = ("future_participation", "feedback_improvements")
        widgets = {
            "future_participation": forms.RadioSelect,
            "feedback_improvements": forms.Textarea(
                attrs={"class": BASE_INPUT_CLASS, "rows": 4}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["future_participation"].choices = Attendance.FutureParticipationChoices.choices
        self.fields["future_participation"].required = True


ATTENDANCE_WIZARD_STEP_FORMS = (
    AttendanceStep1Form,
    AttendanceStep2Form,
    AttendanceStep3Form,
    AttendanceStep4Form,
    AttendanceStep5Form,
)

ATTENDANCE_SATISFACTION_FIELD_NAMES = AttendanceStep3Form.Meta.fields


def _merge_attendance_step_widgets():
    merged = {}
    for form_cls in ATTENDANCE_WIZARD_STEP_FORMS:
        w = getattr(form_cls.Meta, "widgets", None)
        if w:
            merged.update(w)
    return merged


class AttendanceForm(forms.ModelForm):
    """Todos los campos de asistencia (un solo envío); el asistente usa los pasos parciales."""

    class Meta:
        model = Attendance
        exclude = ("event", "created_at")
        widgets = _merge_attendance_step_widgets()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        AttendanceStep3Form.apply_satisfaction_radio_fields(self)
