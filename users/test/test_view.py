from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from users.models import Attendee, Organizer


class RegisterView(APITestCase):

    def setUp(self):
        self.data = {
            "email": "newuser1@app.com",
            "user_type": "organizer",
            "password": "1234567",
            "password2": "1234567"
        }

    def test_register_user(self):
        url = reverse("register")
        response = self.client.post(url, self.data)
        user = get_user_model().objects.get(id=1)
        org = get_object_or_404(Organizer, user=user)

        self.assertEqual(user.email, "newuser1@app.com")

        # Asserts cutom signal automatically creates profile for user
        self.assertEqual(org.user.email, "newuser1@app.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_not_authenticated_permission(self):
        user = get_user_model().objects.create_user(
            email = "newuser1@app.com", 
            user_type = "organizer",
            password = "12345678"
        )
        self.client.force_login(user)
        url = reverse("register")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrganizerProfileTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email = "newuser1@app.com", 
            user_type = "organizer",
            password = "12345678"
        )
        self.client.force_login(self.user)

    def test_get_profile(self):
        url = reverse("organizer-profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_patch_request(self):
        data = {
            "name" : "Sound Organizers"
        }
        url = reverse("organizer-profile")
        response = self.client.patch(url, data)
        org = get_object_or_404(Organizer, user=self.user)
        self.assertEqual(org.name, "Sound Organizers")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AttendeeProfileTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email = "newuser1@app.com", 
            user_type = "attendee",
            password = "12345678"
        )
        self.client.force_login(self.user)

    def test_get_profile(self):
        url = reverse("attendee-profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_patch_request(self):
        data = {
            "contact_phone" : "5555"
        }
        url = reverse("attendee-profile")
        response = self.client.patch(url, data)
        att = get_object_or_404(Attendee, user=self.user)
        self.assertEqual(att.contact_phone, "5555")
        self.assertEqual(response.status_code, status.HTTP_200_OK)