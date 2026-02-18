# Generated manually for Evento -> Event and field renames

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_evento_fecha_fin_alter_evento_fecha_inicio"),
    ]

    operations = [
        migrations.RenameModel(old_name="Evento", new_name="Event"),
        migrations.RenameField(model_name="event", old_name="nombre", new_name="name"),
        migrations.RenameField(model_name="event", old_name="fecha_inicio", new_name="start_date"),
        migrations.RenameField(model_name="event", old_name="fecha_fin", new_name="end_date"),
        migrations.RenameField(model_name="event", old_name="area_responsable", new_name="responsible_area"),
        migrations.RenameField(model_name="event", old_name="participantes_esperados", new_name="expected_participants"),
        migrations.RenameField(model_name="event", old_name="descripcion", new_name="description"),
        migrations.RenameField(model_name="event", old_name="creado_en", new_name="created_at"),
        migrations.RenameField(model_name="event", old_name="actualizado_en", new_name="updated_at"),
    ]
