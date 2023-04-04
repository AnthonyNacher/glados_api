from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import EntitySerializer
from rest_framework.response import Response
from rest_framework.views import APIView


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
    
def PageNotFoundView(request, exception):
        data = {"status_code" : 404, "error": "not_found", "message" : "Resource not found."}
        return JsonResponse(data)