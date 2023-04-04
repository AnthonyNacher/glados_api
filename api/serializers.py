from api.models import Entity
from rest_framework import serializers

# from https://www.django-rest-framework.org/api-guide/serializers/ 
class EntitySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    type = serializers.CharField(source="get_type")
    status = serializers.CharField(source="get_status")

    class Meta : 
        model = Entity
        fields = ['id', 'name', 'type', 'status', 'value', 'created_at']
          