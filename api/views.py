import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import EntitySerializer, RoomSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
from .models import Entity, Room
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
    
    
            
@method_decorator(csrf_exempt, name='dispatch')
class EntityAPI(APIView):
    def get(self,request, entity_uuid):
        try :
            instance = Entity.objects.get(id=entity_uuid)
            serializer = EntitySerializer(instance)
            return Response(serializer.data, status=200)
        except Entity.DoesNotExist:
            return PageNotFoundView(request, Entity.DoesNotExist)
    def delete(self, request, entity_uuid):
        # We want to execute delete on the Entity in case we're later modifying deletion (soft delete for example)
        try :
            instance = Entity.objects.get(id=entity_uuid)
            instance.delete()
        except Entity.DoesNotExist:
            pass
        response = Response()
        response.status_code = 204
        return response
    
    def put(self, request, entity_uuid):
        try:
            entity = Entity.objects.get(id=entity_uuid)

            serializer = EntitySerializer(entity, data=request.data)
            if serializer.is_valid():
                serializer.save()
                updated_entity = Entity.objects.get(id=entity_uuid)
                request_room = Room.objects.get(id=request.data.get("room"))

                if updated_entity.room != request_room:
                    updated_entity.room = request_room
                    updated_entity.save()
                    serializer = EntitySerializer(updated_entity)
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
class RoomsAPI(APIView):
    def get(self, request):
        rooms = Room.objects.all().exclude(id=Room.get_not_assigned_room_id())

        serialized_room = RoomSerializer(rooms, many=True)
        return Response(serialized_room.data)
    def post(self, request):
        serialized_new_room = RoomSerializer(data=request.data)
        if serialized_new_room.is_valid():
            serialized_new_room.save()
            return Response(serialized_new_room.data, status=status.HTTP_201_CREATED)
        return Response(serialized_new_room.errors, status=status.HTTP_400_BAD_REQUEST)
    
def PageNotFoundView(request, exception):
        data = {"error": "not_found", "message" : "Resource not found."}
        return HttpResponseNotFound(json.dumps(data), content_type='application/json')

       
@method_decorator(csrf_exempt, name='dispatch')
class RoomAPI(APIView):
    def get(self,request, room_uuid):
        if room_uuid == Room.get_not_assigned_room_id():
            return Response(status=403)
        try :
            instance = Room.objects.get(id=room_uuid)
            serializer = RoomSerializer(instance)
            return Response(serializer.data, status=200)
        except Room.DoesNotExist:
            return PageNotFoundView(request, Room.DoesNotExist)
        
    def delete(self, request, room_uuid):
        if room_uuid == Room.get_not_assigned_room_id():
            return Response(status=403)
        
        # .delete for softdelete later (see Entity)
        try :
            instance = Room.objects.get(id=room_uuid)
            instance.delete()
        except Room.DoesNotExist:
            pass
        response = Response()
        response.status_code = 204
        return response
    
    def put(self, request, room_uuid):
        if room_uuid == Room.get_not_assigned_room_id():
            return Response(status=403)
        try:
            room = Room.objects.get(id=room_uuid)

            serializer = RoomSerializer(room, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)
        except Room.DoesNotExist:
            serializer = RoomSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
    
def TextToSpeechResume(request):
        tts_speech = "Voici toutes les entités présentes."
        end_speech = ""
        for room in Room.objects.all():
            if room.id == Room.get_not_assigned_room_id():
                default_room_entities_count = Entity.objects.filter(room=Room.get_not_assigned_room_id()).count()
                if default_room_entities_count > 0:
                    end_speech = "En revanche, certains appareils ne sont pas encore assignés à une pièce."
                    for entity in Entity.objects.filter(room=Room.get_not_assigned_room_id()) :
                        end_speech += entity.get_tts()
            else : 
                tts_speech += room.get_tts()
                for entity in Entity.objects.filter(room=room) :
                    tts_speech += entity.get_tts()
        final_speech = tts_speech + end_speech
            
        return JsonResponse(data= {"text" : final_speech})