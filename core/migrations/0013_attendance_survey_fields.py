# Generated manually for Attendance survey fields

import django.core.validators
from django.db import migrations, models

_SATISFACTION_VALIDATORS = [
    django.core.validators.MinValueValidator(1),
    django.core.validators.MaxValueValidator(5),
]


def copy_legacy_satisfaction_and_comments(apps, schema_editor):
    Attendance = apps.get_model("core", "Attendance")
    for att in Attendance.objects.all():
        s = att.satisfaction
        if s is None:
            s = 3
        att.satisfaction_methodology = s
        att.satisfaction_session_usefulness = s
        att.satisfaction_schedule_timing = s
        att.satisfaction_logistics = s
        att.satisfaction_activity_usefulness = s
        att.accepts_data_processing = True
        if att.comments:
            att.feedback_improvements = att.comments
        att.save(
            update_fields=[
                "satisfaction_methodology",
                "satisfaction_session_usefulness",
                "satisfaction_schedule_timing",
                "satisfaction_logistics",
                "satisfaction_activity_usefulness",
                "accepts_data_processing",
                "feedback_improvements",
            ]
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_activity_event_participation_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="accepts_data_processing",
            field=models.BooleanField(
                default=False,
                verbose_name="Aceptación del tratamiento de datos personales",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="satisfaction_methodology",
            field=models.PositiveSmallIntegerField(
                null=True,
                validators=_SATISFACTION_VALIDATORS,
                verbose_name="Satisfacción: metodología usada en la sesión (1–5)",
                help_text="1 = muy insatisfecho, 5 = completamente satisfecho.",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="satisfaction_session_usefulness",
            field=models.PositiveSmallIntegerField(
                null=True,
                validators=_SATISFACTION_VALIDATORS,
                verbose_name="Satisfacción: utilidad de la sesión (1–5)",
                help_text="1 = muy insatisfecho, 5 = completamente satisfecho.",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="satisfaction_schedule_timing",
            field=models.PositiveSmallIntegerField(
                null=True,
                validators=_SATISFACTION_VALIDATORS,
                verbose_name="Satisfacción: horario del encuentro y tiempo (1–5)",
                help_text="1 = muy insatisfecho, 5 = completamente satisfecho.",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="satisfaction_logistics",
            field=models.PositiveSmallIntegerField(
                null=True,
                validators=_SATISFACTION_VALIDATORS,
                verbose_name="Satisfacción: organización logística (1–5)",
                help_text="1 = muy insatisfecho, 5 = completamente satisfecho.",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="satisfaction_activity_usefulness",
            field=models.PositiveSmallIntegerField(
                null=True,
                validators=_SATISFACTION_VALIDATORS,
                verbose_name="Satisfacción: utilidad de la actividad (1–5)",
                help_text="1 = muy insatisfecho, 5 = completamente satisfecho.",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="activity_incidence",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "a",
                        "Abrió posibilidades de reflexión frente al conocimiento libre.",
                    ),
                    (
                        "b",
                        "Me generó compromiso con la necesidad de contribuir al conocimiento libre.",
                    ),
                    (
                        "c",
                        "Me animó a cambiar mi comprensión sobre la construcción de conocimiento colaborativo.",
                    ),
                    ("d", "Otro"),
                ],
                max_length=1,
                null=True,
                verbose_name="Incidencia de la actividad",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="activity_incidence_other",
            field=models.TextField(
                blank=True,
                verbose_name="Incidencia (texto si eligió «Otro»)",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="learned_new_aspect",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="Aspecto que no sabía antes del taller",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="interesting_aspect_discuss",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="Aspecto tan interesante que lo discutiría con otras personas",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="future_participation",
            field=models.CharField(
                blank=True,
                choices=[
                    ("yes", "Sí"),
                    ("no", "No"),
                    ("maybe", "Tal vez"),
                ],
                max_length=10,
                null=True,
                verbose_name="¿Participar en futuras actividades de Wikimedia Colombia?",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="feedback_improvements",
            field=models.TextField(
                blank=True,
                default="",
                verbose_name="Aspectos que podrían mejorarse en futuras actividades",
            ),
        ),
        migrations.RunPython(copy_legacy_satisfaction_and_comments, noop_reverse),
        migrations.RemoveField(
            model_name="attendance",
            name="satisfaction",
        ),
        migrations.RemoveField(
            model_name="attendance",
            name="comments",
        ),
        migrations.AlterField(
            model_name="attendance",
            name="satisfaction_methodology",
            field=models.PositiveSmallIntegerField(
                validators=_SATISFACTION_VALIDATORS,
                verbose_name="Satisfacción: metodología usada en la sesión (1–5)",
                help_text="1 = muy insatisfecho, 5 = completamente satisfecho.",
            ),
        ),
        migrations.AlterField(
            model_name="attendance",
            name="satisfaction_session_usefulness",
            field=models.PositiveSmallIntegerField(
                validators=_SATISFACTION_VALIDATORS,
                verbose_name="Satisfacción: utilidad de la sesión (1–5)",
                help_text="1 = muy insatisfecho, 5 = completamente satisfecho.",
            ),
        ),
        migrations.AlterField(
            model_name="attendance",
            name="satisfaction_schedule_timing",
            field=models.PositiveSmallIntegerField(
                validators=_SATISFACTION_VALIDATORS,
                verbose_name="Satisfacción: horario del encuentro y tiempo (1–5)",
                help_text="1 = muy insatisfecho, 5 = completamente satisfecho.",
            ),
        ),
        migrations.AlterField(
            model_name="attendance",
            name="satisfaction_logistics",
            field=models.PositiveSmallIntegerField(
                validators=_SATISFACTION_VALIDATORS,
                verbose_name="Satisfacción: organización logística (1–5)",
                help_text="1 = muy insatisfecho, 5 = completamente satisfecho.",
            ),
        ),
        migrations.AlterField(
            model_name="attendance",
            name="satisfaction_activity_usefulness",
            field=models.PositiveSmallIntegerField(
                validators=_SATISFACTION_VALIDATORS,
                verbose_name="Satisfacción: utilidad de la actividad (1–5)",
                help_text="1 = muy insatisfecho, 5 = completamente satisfecho.",
            ),
        ),
        migrations.AlterField(
            model_name="attendance",
            name="feedback_improvements",
            field=models.TextField(
                blank=True,
                verbose_name="Aspectos que podrían mejorarse en futuras actividades",
            ),
        ),
    ]
