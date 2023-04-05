from django.test import TestCase

from rest_framework.test import APIClient

class APITestCase (TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_unexistingè_resource(self):
        response = self.client.get('/unexisting-resouce')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error" : "not_found", "message" : "Resource not found."})

    def test_get_version(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"version" : "1.0"})
        