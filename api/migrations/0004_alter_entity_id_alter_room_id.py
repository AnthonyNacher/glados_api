# Generated by Django 4.1.7 on 2023-04-04 19:32

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_entity_id_alter_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='id',
            field=models.UUIDField(default=api.models.get_uuid_as_hex, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.UUIDField(default=api.models.get_uuid_as_hex, primary_key=True, serialize=False),
        ),
    ]
