# Generated by Django 4.1.7 on 2023-04-05 22:12

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_entity_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='id',
            field=models.UUIDField(default=api.models.get_uuid_as_hex, editable=False, primary_key=True, serialize=False),
        ),
    ]
