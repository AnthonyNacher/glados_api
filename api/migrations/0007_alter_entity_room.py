# Generated by Django 4.1.7 on 2023-04-06 23:15

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_entity_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='room',
            field=models.ForeignKey(default=api.models.Entity.get_not_assigned_room, on_delete=django.db.models.deletion.CASCADE, to='api.room'),
        ),
    ]
