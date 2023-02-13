from rest_framework.test import APITestCase
from . import models

from users.models import User

 
class TestAmenties(APITestCase):
    
    NAME = "Amenity Test"
    DESC = "Amenty Des"
    
    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )
    
    def test_all_amentities(self):
        response = self.client.get("/api/v1/rooms/amenities/")
        # print(response)
        data = response.json()
        
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200",
        )
        self.assertIsInstance(data, list)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESC,)
        
    def test_amenity_not_found(self):
        response = self.client.get("/api/v1/rooms/amenities/2")
        self.assertEqual(response.status_code, 404)
        
    def test_get_amenity(self):
        
        response = self.client.get("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        self.assertEqual(data["name"], self.NAME)
        self.assertEqual(data["description"], self.DESC) 
        
    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 204)
        
    def test_put_amenity(self):
        # your code challenge
        pass        
    
class TestRooms(APITestCase):
    def setUp(self):
        user = User.objects.create(
            username="test",
        )
        user.set_password("123")
        user.save()
        self.user = user

    def test_create_room(self):

        response = self.client.post("/api/v1/rooms/")

        self.assertEqual(response.status_code, 403)

        self.client.force_login(
            self.user,
        )    