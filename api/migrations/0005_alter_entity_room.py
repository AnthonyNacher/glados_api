# Generated by Django 4.1.7 on 2023-04-05 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_entity_id_alter_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.room'),
        ),
    ]
