# Generated by Django 4.1.7 on 2023-04-06 23:46

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_entity_room'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entity',
            options={'verbose_name': 'Appareil', 'verbose_name_plural': 'Appareils'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name': 'Pièce', 'verbose_name_plural': 'Pièces'},
        ),
        migrations.AlterField(
            model_name='entity',
            name='room',
            field=models.ForeignKey(default=api.models.get_not_assigned_room_id, on_delete=django.db.models.deletion.CASCADE, to='api.room'),
        ),
    ]
