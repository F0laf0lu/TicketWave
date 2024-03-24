from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Organizer, Attendee
import os
from django import setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketwave.testsettings')
setup()

# Create your tests here. 

class CustomUserTests(TestCase):
    '''All Tests user creation with the database'''

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email = 'testuser@app.com',
            password = 'testuser',
        )

        self.user1 = User.objects.create_user(
            email = 'testuser1@app.com',
            password = 'testuser',
            user_type = 'organizer'
        )

        self.user2 = User.objects.create_user(
            email = 'testuser2@app.com',
            password = 'testuser',
            user_type = 'attendee'
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, 'testuser@app.com')
        self.assertIsNone(self.user.user_type)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_verified)

    def test_organizer_profile_created(self):
        user = Organizer.objects.get(user=self.user1)
        self.assertTrue(user)

    def test_attendee_profile_created(self):
        user = Attendee.objects.get(user=self.user2)
        self.assertTrue(user)

    def test_update_created_profile(self):
        organizer = Organizer.objects.get(user=self.user1)
        organizer.name = 'Sunny Events'
        organizer.save()

        updated_organizer = Organizer.objects.get(user=self.user1)
        self.assertEqual(updated_organizer.name, 'Sunny Events')

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            email = "admin@site.com",
            password = "testadmin",
        )

        self.assertEqual(user.email, 'admin@site.com')
        self.assertEqual(user.user_type, None)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_verified)

