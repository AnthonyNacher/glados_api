from django.db import models
import uuid
# Create your models here.

def get_uuid_as_hex():
    return uuid.uuid4().hex

class Entity (models.Model):
    READABLE_TYPES = {
        "sensor" : "1",
        "light" : "2",
        "switch" : "3",
        "multimedia" : "4",
        "air_conditioner" : "5",
        }
    TYPES = [
        ('1', 'sensor'),
        ('2', 'light'),
        ('3', 'switch'),
        ('4', 'multimedia'),
        ('5', 'air_conditioner'),
    ]
    
    READABLE_STATUS = {
        "on" : "1",
        "off" : "2",
        "unavailable" : "3",
        }
    STATUS = [
        ('1', 'on'),
        ('2', 'off'),
        ('3', 'unavailable'),
    ]

    id = models.UUIDField(primary_key=True, default=get_uuid_as_hex, editable=False)
    name = models.CharField(max_length=600, null=False)
    type = models.CharField(max_length=1, choices=TYPES, null=False)
    status = models.CharField(max_length=1, choices=STATUS, null=False)
    value =  models.CharField(max_length=600, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey("Room", on_delete=models.CASCADE, null=True)
    def get_status(self):
        return self.get_status_display()
    def get_type(self):
        return self.get_type_display()
    
class Room (models.Model):
    id = models.UUIDField(primary_key=True, default=get_uuid_as_hex)
    name = models.CharField(max_length=600, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

