from unittest.mock import Mock, patch
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from users.models import Attendee, Organizer
from users.utils import send_code_to_user


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

    def test_passord_does_not_match(self):
        data = {
            "email": "newuser2@app.com",
            "user_type": "organizer",
            "password": "1234567",
            "password2": "123456"
        }
        url = reverse("register")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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

class EmailVerification(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email = "newuser1@app.com", 
            user_type = "attendee",
            password = "12345678",
            secret_key="1-abcdef"
        )
        self.client.force_login(self.user)

    @patch('users.views.send_code_to_user') #mock send_code_to_user(email) func in views 
    def test_send_code(self, mock_send_code_to_user):
        # @pactch decorator replaces mock_send_code_to_user ith a mock obj of send-code_to_user function

        url = reverse('verify-email')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock_send_code_to_user.called) #Check func was called
        mock_send_code_to_user.assert_called_once_with(self.user.email)
        #called with correct parameter


    def test_verify_email_permission_denied(self):
        # Test when the user is already verified (permission should deny access)
        self.user.is_verified = True
        self.user.save()

        url = reverse('verify-email')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    @patch('users.views.pyotp.HOTP') 
    def test_verify_email(self, mock_hotp):
        otp_code = '123456'

        mock_hotp_instance = Mock()
        mock_hotp_instance.verify.return_value = True
        mock_hotp.return_value = mock_hotp_instance
        
        url = reverse('verify')
        response = self.client.post(url, {'otp': otp_code})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Email verification successful')

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
        mock_hotp_instance.verify.assert_called_once_with(otp_code, int(self.user.secret_key.split('-')[0]))



    @patch('users.views.pyotp.HOTP')
    def test_invalid_otp(self, mock_hotp):
        otp_code = '123456'
        
        hotp = Mock() #instantiate a mock class
        hotp.verify.return_value = False #modify verify method like for pyotp.Hotp

        mock_hotp.return_value = hotp 
        #hen mock_hotp from parameter is used, set return value to instantiated class
        
        url = reverse('verify')
        response = self.client.post(url, {'otp': otp_code})

        self.user.refresh_from_db()

        self.assertFalse(self.user.is_verified)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        hotp.verify.assert_called_once_with(otp_code, int(self.user.secret_key.split('-')[0]))