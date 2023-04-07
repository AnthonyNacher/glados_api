"""glados URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import ReturnAPIVersion, EntitiesAPI, EntityAPI, RoomsAPI, RoomAPI
urlpatterns = [
    path('', ReturnAPIVersion.as_view(), name="get_api_version"),
    path('rooms', RoomsAPI.as_view(), name="api_rooms"),
    path('rooms/<uuid:room_uuid>', RoomAPI.as_view(), name="api_room"),
    path('entities', EntitiesAPI.as_view(), name="api_entities"),
    path('entities/<uuid:entity_uuid>', EntityAPI.as_view(), name="api_entity"),
]
