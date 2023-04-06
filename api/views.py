import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import EntitySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
from .models import Entity
from django.views.generic import View

@method_decorator(csrf_exempt, name='dispatch')
class ReturnAPIVersion(View):
    def get(self, request):
        data = {"version": "1.0"}
        return JsonResponse(data)
    
@method_decorator(csrf_exempt, name='dispatch')
class EntitiesAPI(APIView):
    def get(self, request):
        entities = Entity.objects.all()

        # Filter by type
        type_filter = self.request.GET.get('type', None)
        if type_filter is not None :
            if  type_filter in Entity.READABLE_TYPES.keys():
                entities = entities.filter(type=Entity.READABLE_TYPES[type_filter])
            else :
                entities = []
            
        
        # Filter by status
        status_filter = self.request.GET.get('status', None)
        if status_filter is not None :
            if  status_filter in Entity.READABLE_STATUS.keys():
                entities = entities.filter(status=Entity.READABLE_STATUS[status_filter])
            else :
                entities = []


        # Filter by room
        room_filter = self.request.GET.get('room', None)
        if room_filter is not None :
            entities = entities.filter(room__name__contains=room_filter)


        serialized_entity = EntitySerializer(entities, many=True)
        return Response(serialized_entity.data)
    def post(self, request):
        
        serialized_new_entity = EntitySerializer(data=request.data)
        if serialized_new_entity.is_valid():
            serialized_new_entity.save()
            
            return Response(serialized_new_entity.data, status=status.HTTP_201_CREATED)
        return Response(serialized_new_entity.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        entity_id = request.data.get('id', None)
        try:
            entity = Entity.objects.get(id=entity_id)
            serializer = EntitySerializer(entity, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)
        except Entity.DoesNotExist:
            serializer = EntitySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
            
@method_decorator(csrf_exempt, name='dispatch')
class EntityAPI(APIView):
    def delete(self, request, entity_uuid):
        # We want to execute delete on the Entity in case we're later modifying deletion (soft delete for example)
        try :
            instance = Entity.objects.get(id=entity_uuid)
        except Entity.DoesNotExist:
            pass
        instance.delete()
        response = Response()
        response.status_code = 204
        return response
    
    
def PageNotFoundView(request, exception):
        data = {"error": "not_found", "message" : "Resource not found."}
        return HttpResponseNotFound(json.dumps(data), content_type='application/json')