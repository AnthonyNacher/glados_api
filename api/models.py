from django.db import models
import uuid
# Create your models here.

def get_uuid_as_hex():
    return uuid.uuid4().hex

def get_not_assigned_room_id():
        default_uuid = uuid.UUID(int=1)
        default_uuid_hex_as_str = str(default_uuid.hex)
        try : 
            instance = Room.objects.get(id=default_uuid_hex_as_str)
        except Room.DoesNotExist:
            instance = Room.objects.create(id=default_uuid_hex_as_str, name="NO ROOM")
        instance.save()
        return instance.id
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
    def get_not_assigned_room():
        return get_not_assigned_room_id()
    id = models.UUIDField(primary_key=True, default=get_uuid_as_hex, editable=False)
    name = models.CharField(max_length=600, null=False)
    type = models.CharField(max_length=1, choices=TYPES, null=False)
    status = models.CharField(max_length=1, choices=STATUS, null=False)
    value =  models.CharField(max_length=600, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey("Room", on_delete=models.CASCADE, null=False, default=get_not_assigned_room_id)
    def get_status(self):
        return self.get_status_display()
    def get_type(self):
        return self.get_type_display()
    class Meta:
        verbose_name="Appareil"
        verbose_name_plural="Appareils"
    def __str__(self):
        return f"{self.id} - {self.name} - (type : {self.type} / statut : {self.status} / valeur : {self.value})"
    
class Room (models.Model):
    id = models.UUIDField(primary_key=True, default=get_uuid_as_hex)
    name = models.CharField(max_length=600, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name="Pièce"
        verbose_name_plural="Pièces"    
    def __str__(self):
        return f"{self.id} - {self.name}"