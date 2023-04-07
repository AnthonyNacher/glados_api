from api.models import Entity, Room, get_not_assigned_room_id
from rest_framework import serializers

# from https://www.django-rest-framework.org/api-guide/serializers/ 

# Based on this, inserting with value means we need to customize the serialier's ChoiceField : 
# https://stackoverflow.com/questions/28945327/django-rest-framework-with-choicefield

class CustomChoiceField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_choice'] = 'Choice is invalid.'
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]
    def to_internal_value(self, data):
        if data == '' and self.allow_blank :
            return ''
        
        # For example, sensor is binded to 1, so we check if the sensor exists, and if it exists in choices, we return the key (1 in our example here)
        for key, val in self._choices.items() : 
            if val == data :
                return key
        self.fail('invalid_choice', input=data)

class RoomSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Room
        fields = ["id", "name"]
    
class EntitySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False, read_only=True)
    type = CustomChoiceField(choices=Entity.TYPES)
    status = CustomChoiceField(choices=Entity.STATUS)
    value = serializers.CharField(allow_blank=True, required=False)
    id = serializers.UUIDField(format="hex_verbose", read_only=True)
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    class Meta : 
        model = Entity
        fields = ['id', 'name', 'type', 'status', 'value', 'created_at', 'room']