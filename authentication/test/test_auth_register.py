from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

class AuthRegisterTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("authviewset-register")

    def test_register_success(self):
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_register_existing_user(self):
        get_user_model().objects.create_user(username="existinguser", password="password")
        response = self.client.post(self.register_url, {"username": "existinguser", "password": "password"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Username already exists"})

    def test_register_missing_fields(self):
        response = self.client.post(self.register_url, {"username": "user"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Username and password are required"})
