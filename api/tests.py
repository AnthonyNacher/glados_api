from django.test import TestCase

# Create your tests here.
from api.models import Entity, Room
from rest_framework.test import APIClient

class APITestCase (TestCase):
    def setUp(self):
        kitchen = Room(id="11111111-1111-1111-1111-111111111110", name="Kitchen")
        kitchen.save()

        living_room = Room(id="11111111-1111-1111-1111-111111111101", name="Living Room")
        living_room.save()

        entity = Entity(
            id="00000000-0000-0000-0000-000000000001",
            name="Ceiling Light",
            type=Entity.READABLE_TYPES["light"],
            status=Entity.READABLE_STATUS["off"],
            value=None,
            room_id=kitchen.id,
            created_at='')
        entity.save()
        entity.created_at="2023-04-04T21:17:56"
        entity.save()

        entity = Entity(
            id="00000000-0000-0000-0000-000000000002",
            name="Lamp",
            type=Entity.READABLE_TYPES["light"],
            status=Entity.READABLE_STATUS["on"],
            value=200,
            room_id=living_room.id,
            created_at='')
        entity.save()
        entity.created_at="2023-04-04T21:17:56"
        entity.save()
        entity = Entity(
            id="00000000-0000-0000-0000-000000000003",
            name="Thermometer",
            type=Entity.READABLE_TYPES["sensor"],
            status=Entity.READABLE_STATUS["on"],
            value=28,
            room_id=living_room.id,
            created_at='')
        
        entity.save()
        entity.created_at="2023-04-04T21:17:56"
        entity.save()

    def test_get_entities(self):
        response = self.client.get("/entities")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
                                [{
                    "id": "00000000-0000-0000-0000-000000000001",
                    "name": "Ceiling Light",
                    "type": "light",
                    "status": "off",
                    "value": None,
                    "created_at": "2023-04-04T21:17:56",
                    "room" : "11111111-1111-1111-1111-111111111110"
                },
                {
                    "id": "00000000-0000-0000-0000-000000000002",
                    "name": "Lamp",
                    "type": "light",
                    "status": "on",
                    "value": "200",
                    "created_at": "2023-04-04T21:17:56",
                    "room" : "11111111-1111-1111-1111-111111111101"
                },
                {
                    "id": "00000000-0000-0000-0000-000000000003",
                    "name": "Thermometer",
                    "type": "sensor",
                    "status": "on",
                    "value": "28",
                    "created_at": "2023-04-04T21:17:56",
                    "room" : "11111111-1111-1111-1111-111111111101"
                }])
    def test_get_entities_with_type_filter(self):
        response = self.client.get("/entities?type=sensor")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
                                            [
                            {
                                "id": "00000000-0000-0000-0000-000000000003",
                                "name": "Thermometer",
                                "type": "sensor",
                                "status": "on",
                                "value": "28",
                                "created_at": "2023-04-04T21:17:56",
                                "room" : "11111111-1111-1111-1111-111111111101"
                            }
                        ])
        
    def test_get_entities_with_status_filter(self):
        response = self.client.get("/entities?status=on")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
                                            [
                            {
                                "id": "00000000-0000-0000-0000-000000000002",
                                "name": "Lamp",
                                "type": "light",
                                "status": "on",
                                "value": "200",
                                "created_at": "2023-04-04T21:17:56",
                                "room" : "11111111-1111-1111-1111-111111111101"
                            },
                            {
                                "id": "00000000-0000-0000-0000-000000000003",
                                "name": "Thermometer",
                                "type": "sensor",
                                "status": "on",
                                "value": "28",
                                "created_at": "2023-04-04T21:17:56",
                                "room" : "11111111-1111-1111-1111-111111111101"
                            }
                        ])
        
    def test_get_entities_with_room_filter(self):
        response = self.client.get("/entities?room=Living Room")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
                                            [
                            {
                                "id": "00000000-0000-0000-0000-000000000002",
                                "name": "Lamp",
                                "type": "light",
                                "status": "on",
                                "value": "200",
                                "created_at": "2023-04-04T21:17:56",
                                "room" : "11111111-1111-1111-1111-111111111101"
                            },
                            {
                                "id": "00000000-0000-0000-0000-000000000003",
                                "name": "Thermometer",
                                "type": "sensor",
                                "status": "on",
                                "value": "28",
                                "created_at": "2023-04-04T21:17:56",
                                "room" : "11111111-1111-1111-1111-111111111101"
                            }
                        ])
        
    def test_get_entities_with_wrong_status_filter_(self):
        response = self.client.get("/entities?status=thisonedoesntexist")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
    def test_get_entities_with_wrong_type_filter_(self):
        response = self.client.get("/entities?type=thisonedoesntexist")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
    def test_get_entities_with_wrong_room_filter_(self):
        response = self.client.get("/entities?room=thisonedoesntexist")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
    
    

    def test_post_entity(self):
        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        self.assertEqual(INITIAL_ENTITY_COUNT, 3)

        response = self.client.post("/entities", {
                    "name": "Airton Pack Mono-split R32-5270",
                    "type": "air_conditioner",
                    "status": "off",
                    "value": "1189",
                    "room" : "11111111-1111-1111-1111-111111111101"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(INITIAL_ENTITY_COUNT + 1, len(Entity.objects.all()))
    def test_post_entity_with_new_room(self):
        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        self.assertEqual(INITIAL_ENTITY_COUNT, 3)

        response = self.client.post("/entities", {
                    "name": "Airton Pack Mono-split R32-5270",
                    "type": "air_conditioner",
                    "status": "off",
                    "value": "1189",
                    "room" : "11111111-1111-1111-1111-111111111001"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(INITIAL_ENTITY_COUNT, len(Entity.objects.all()))
 
    def test_post_entity_minimal_data(self):
        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        self.assertEqual(INITIAL_ENTITY_COUNT, 3)

        response = self.client.post("/entities", {
                    "name": "Airton Pack Mono-split R32-5270",
                    "type": "air_conditioner",
                    "status": "off",
                    "room" : "11111111-1111-1111-1111-111111111101"
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(INITIAL_ENTITY_COUNT + 1, len(Entity.objects.all()))

    def test_post_entity_missing_data_status(self):
        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        self.assertEqual(INITIAL_ENTITY_COUNT, 3)

        response = self.client.post("/entities", {
                    "name": "Airton Pack Mono-split R32-5270",
                    "type": "air_conditioner",
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(INITIAL_ENTITY_COUNT, len(Entity.objects.all()))

    def test_post_entity_missing_data_type(self):
        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        self.assertEqual(INITIAL_ENTITY_COUNT, 3)

        response = self.client.post("/entities", {
                    "name": "Airton Pack Mono-split R32-5270",
                    "status": "on",
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(INITIAL_ENTITY_COUNT, len(Entity.objects.all()))

    def test_post_entity_missing_data_name(self):
        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        self.assertEqual(INITIAL_ENTITY_COUNT, 3)

        response = self.client.post("/entities", {
                    "status": "on",
                    "type": "air_conditioner",
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(INITIAL_ENTITY_COUNT, len(Entity.objects.all()))

    def test_post_entity_minimal_data_but_wrong_status(self):
        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        self.assertEqual(INITIAL_ENTITY_COUNT, 3)

        response = self.client.post("/entities", {
                    "name": "Airton Pack Mono-split R32-5270",
                    "type": "air_conditioner",
                    "status": "thisisdefinitlynotanexistingstatus"
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(INITIAL_ENTITY_COUNT, len(Entity.objects.all()))
        
    def test_post_entity_minimal_data_but_wrong_type(self):
        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        self.assertEqual(INITIAL_ENTITY_COUNT, 3)

        response = self.client.post("/entities", {
                    "name": "Airton Pack Mono-split R32-5270",
                    "type": "ahousetypeofdevicewouldntbepossibleright",
                    "status": "off"
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(INITIAL_ENTITY_COUNT, len(Entity.objects.all()))
    
    def test_put_on_existing_entity (self):
        tested_entity = Entity.objects.get(id="00000000-0000-0000-0000-000000000001")
        INITIAL_ENTITY_ID = tested_entity.id
        INITIAL_ENTITY_NAME = tested_entity.name
        INITIAL_ENTITY_TYPE = tested_entity.type
        INITIAL_ENTITY_STATUS = tested_entity.status
        INITIAL_ENTITY_VALUE = tested_entity.value
        INITIAL_ENTITY_ROOM = tested_entity.room

        response = self.client.put("/entities/00000000-0000-0000-0000-000000000001", {
                    "id" : "00000000-0000-0000-0000-000000000001",
                    "name": "New Name",
                    "type": "sensor",
                    "status": "unavailable",
                    "value": "100",
                    "room" : "11111111-1111-1111-1111-111111111101"
        },
        content_type='application/json')
        tested_entity_after_put = Entity.objects.get(id="00000000-0000-0000-0000-000000000001")

        # When the PUT is successful on an existing resource, it should return 200
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(INITIAL_ENTITY_ID, tested_entity_after_put.id)
        self.assertNotEqual(INITIAL_ENTITY_NAME, tested_entity_after_put.name)
        self.assertNotEqual(INITIAL_ENTITY_TYPE, tested_entity_after_put.type)
        self.assertNotEqual(INITIAL_ENTITY_STATUS, tested_entity_after_put.status)
        self.assertNotEqual(INITIAL_ENTITY_VALUE, tested_entity_after_put.value)
        self.assertNotEqual(INITIAL_ENTITY_ROOM, tested_entity_after_put.room)

    def test_put_on_nonexistant_entity (self):

        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        response = self.client.put("/entities/00000000-0000-0000-0000-000000000004", {
                    "id" : "00000000-0000-0000-0000-000000000004",
                    "name": "New Entity",
                    "type": "light",
                    "status": "unavailable",
                    "value": "100",
                    "room" : "11111111-1111-1111-1111-111111111110"
        },
        content_type='application/json')
        # When the PUT is successful on a new resource, it should return 201
        self.assertEqual(response.status_code, 201) 
        self.assertEqual(INITIAL_ENTITY_COUNT + 1, len(Entity.objects.all()))
    
    def test_get_entity(self):
        response = self.client.get("/entities/00000000-0000-0000-0000-000000000001")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
                                {
                    "id": "00000000-0000-0000-0000-000000000001",
                    "name": "Ceiling Light",
                    "type": "light",
                    "status": "off",
                    "value": None,
                    "created_at": "2023-04-04T21:17:56",
                    "room" : "11111111-1111-1111-1111-111111111110"
                                })
    def test_get_nonexistant_entity(self):
        response = self.client.get("/entities/00000000-0000-0000-0000-000000000004")
        self.assertEqual(response.status_code, 404)

    def test_delete_entity(self):
        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        self.assertEqual(INITIAL_ENTITY_COUNT, 3)

        response = self.client.delete("/entities/00000000-0000-0000-0000-000000000001")
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(INITIAL_ENTITY_COUNT - 1, len(Entity.objects.all()))

    def test_get_rooms(self):

        response = self.client.get("/rooms")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
                                [{
                    "id": "11111111-1111-1111-1111-111111111110",
                    "name": "Kitchen",
                },
                {
                    "id": "11111111-1111-1111-1111-111111111101",
                    "name": "Living Room",
                }
                ])
    def test_post_rooms(self):
        INITIAL_ROOM_COUNT = len(Entity.objects.all())
        # theres a default room so 2 initialized + 1 default
        self.assertEqual(INITIAL_ROOM_COUNT, 3)

        response = self.client.post("/rooms", {
                    "name": "New room",
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(INITIAL_ROOM_COUNT + 1, len(Room.objects.all()))
    def test_post_rooms_with_invalid_name(self):
        INITIAL_ROOM_COUNT = len(Room.objects.all())
        # theres a default room so 2 initialized + 1 default
        self.assertEqual(INITIAL_ROOM_COUNT, 3)

        response = self.client.post("/rooms", {
                    "name": "",
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(INITIAL_ROOM_COUNT, len(Room.objects.all()))
    
    def test_get_room(self):
        response = self.client.get("/rooms/11111111-1111-1111-1111-111111111101")
        self.assertEqual(response.status_code, 200)

    def test_get_default_room(self):
        response = self.client.get("/rooms/" + str(Room.get_not_assigned_room_id()))
        self.assertEqual(response.status_code, 403)

    def test_get_nonexistant_room(self):
        response = self.client.get("/rooms/00000000-0000-0000-0000-111111001114")
        self.assertEqual(response.status_code, 404)

    def test_delete_room(self):
        INITIAL_ROOM_COUNT = len(Room.objects.all())
        self.assertEqual(INITIAL_ROOM_COUNT, 3)

        response = self.client.delete("/rooms/11111111-1111-1111-1111-111111111101")
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(INITIAL_ROOM_COUNT - 1, len(Room.objects.all()))
    def test_delete_default_room(self):
        INITIAL_ROOM_COUNT = len(Room.objects.all())
        self.assertEqual(INITIAL_ROOM_COUNT, 3)

        response = self.client.get("/rooms/" + str(Room.get_not_assigned_room_id()))
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(INITIAL_ROOM_COUNT, len(Room.objects.all()))


    def test_put_on_existing_room (self):
        tested_room = Room.objects.get(id="11111111-1111-1111-1111-111111111101")
        INITIAL_ROOM_NAME = tested_room.name

        response = self.client.put("/rooms/11111111-1111-1111-1111-111111111101", {
                    "name": "New Name",
        },
        content_type='application/json')
        tested_room_after_put = Room.objects.get(id="11111111-1111-1111-1111-111111111101")

        # When the PUT is successful on an existing resource, it should return 200
        self.assertEqual(response.status_code, 200) 
        self.assertNotEqual(INITIAL_ROOM_NAME, tested_room_after_put.name)
    
    def test_put_on_default_room (self):
        tested_room = Room.objects.get(id=Room.get_not_assigned_room_id())
        INITIAL_ROOM_NAME = tested_room.name

        response = self.client.put("/rooms/" + str(Room.get_not_assigned_room_id()),{
                    "name": "New Name",
        },
        content_type='application/json')
        tested_room_after_put = Room.objects.get(id=Room.get_not_assigned_room_id())

        # When the PUT is successful on an existing resource, it should return 200
        self.assertEqual(response.status_code, 403) 
        self.assertEqual(INITIAL_ROOM_NAME, tested_room_after_put.name)

    def test_put_on_nonexistant_room (self):

        INITIAL_ROOM_COUNT = len(Room.objects.all())
        response = self.client.put("/rooms/11111111-1111-1111-1111-111111001114", {
                    "name": "This is a new room",
        },
        content_type='application/json')
        # When the PUT is successful on a new resource, it should return 201
        self.assertEqual(response.status_code, 201) 
        self.assertEqual(INITIAL_ROOM_COUNT + 1, len(Room.objects.all()))