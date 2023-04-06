from django.test import TestCase

# Create your tests here.
from api.models import Entity, Room
from api.models import get_uuid_as_hex
from rest_framework.test import APIClient

class APITestCase (TestCase):
    def setUp(self):
        kitchen = Room(id=get_uuid_as_hex(), name="Kitchen")
        kitchen.save()

        living_room = Room(id=get_uuid_as_hex(), name="Living Room")
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
                    "created_at": "2023-04-04T21:17:56"
                },
                {
                    "id": "00000000-0000-0000-0000-000000000002",
                    "name": "Lamp",
                    "type": "light",
                    "status": "on",
                    "value": "200",
                    "created_at": "2023-04-04T21:17:56"
                },
                {
                    "id": "00000000-0000-0000-0000-000000000003",
                    "name": "Thermometer",
                    "type": "sensor",
                    "status": "on",
                    "value": "28",
                    "created_at": "2023-04-04T21:17:56"
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
                                "created_at": "2023-04-04T21:17:56"
                            }
                        ]
                         
                         )
        
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
                                "created_at": "2023-04-04T21:17:56"
                            },
                            {
                                "id": "00000000-0000-0000-0000-000000000003",
                                "name": "Thermometer",
                                "type": "sensor",
                                "status": "on",
                                "value": "28",
                                "created_at": "2023-04-04T21:17:56"
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
                                "created_at": "2023-04-04T21:17:56"
                            },
                            {
                                "id": "00000000-0000-0000-0000-000000000003",
                                "name": "Thermometer",
                                "type": "sensor",
                                "status": "on",
                                "value": "28",
                                "created_at": "2023-04-04T21:17:56"
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
    
    def test_delete_entity(self):
        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        self.assertEqual(INITIAL_ENTITY_COUNT, 3)

        response = self.client.delete("/entities/00000000-0000-0000-0000-000000000001")
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(INITIAL_ENTITY_COUNT - 1, len(Entity.objects.all()))

    def test_post_entity(self):
        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        self.assertEqual(INITIAL_ENTITY_COUNT, 3)

        response = self.client.post("/entities", {
                    "name": "Airton Pack Mono-split R32-5270",
                    "type": "air_conditioner",
                    "status": "off",
                    "value": "1189",
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(INITIAL_ENTITY_COUNT + 1, len(Entity.objects.all()))
 
    def test_post_entity_minimal_data(self):
        INITIAL_ENTITY_COUNT = len(Entity.objects.all())
        self.assertEqual(INITIAL_ENTITY_COUNT, 3)

        response = self.client.post("/entities", {
                    "name": "Airton Pack Mono-split R32-5270",
                    "type": "air_conditioner",
                    "status": "off"
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
        