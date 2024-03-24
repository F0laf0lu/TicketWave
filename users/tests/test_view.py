from unittest.mock import Mock, patch
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from users.models import Attendee, Organizer
import os
from django import setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketwave.testsettings')
setup()


class RegisterView(APITestCase):

    def setUp(self):
        self.data = {
            "email": "newuser1@app.com",
            "user_type": "organizer",
            "password": "1234567",
            "password2": "1234567"
        }

    def test_register_user(self):
        url = reverse("signup")
        response = self.client.post(url, self.data)
        user = get_user_model().objects.get(id=1)
        org = get_object_or_404(Organizer, user=user)

        self.assertEqual(user.email, "newuser1@app.com")

        # Asserts cutom signal automatically creates profile for user
        self.assertEqual(org.user.email, "newuser1@app.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OrganizerProfileTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email = "newuser1@app.com", 
            user_type = "organizer",
            password = "12345678"
        )
        self.client.force_authenticate(self.user)

    def test_get_profile(self):
        url = reverse("user-profile", kwargs={"pk":self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AttendeeProfileTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email = "newuser1@app.com", 
            user_type = "attendee",
            password = "12345678"
        )
        self.client.force_authenticate(self.user)

    def test_get_profile(self):
        url = reverse("user-profile", kwargs={"pk":self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

