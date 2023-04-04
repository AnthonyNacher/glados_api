from django.contrib import admin

# Register your models here.

from .models import Entity, Room

admin.site.register(Entity)
admin.site.register(Room)
