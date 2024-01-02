from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.models import Organizer, Attendee
from core.models import Event, Ticket


class EventsTestCase(APITestCase):
    def setUp(self):
        self.organizer_user = get_user_model().objects.create_user(
            email='organizer@example.com',
            password='password',
            user_type='organizer'
        )
        self.organizer = Organizer.objects.get(user=self.organizer_user)

        # Login User
        self.client.force_login(user=self.organizer_user)

        # Create some events for testing
        self.event1 = Event.objects.create(
            name='Event 1', 
            time = timezone.now(),
            venue='Venue 1',
            ticket_price = "600.00",
            organizer = self.organizer
            )
        
        self.event2 = Event.objects.create(
            name ='Event 2', 
            time = timezone.now(),
            venue='Venue 2',
            ticket_price = "600.00",
            organizer = self.organizer,
            )

    def test_get_events(self):
        url = reverse("events")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_events(self):
        data = {
            "name": "Gaming Tournament",
            "time": "2023-12-27T00:20:28+01:00",
            "venue": "My House, Lagos",
            "ticket_price": "600.00",
            "organizer": self.organizer.pk
        }

        url = reverse("events")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_event_details(self):
        url = reverse("event-detail", kwargs={'event_id':self.event1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_ticket_for_event(self):
        attendee_user = get_user_model().objects.create_user(
            email='attendee@example.com',
            password='password',
            user_type='attendee'
        )
        self.client.force_login(attendee_user)
        attendee = Attendee.objects.get(user=attendee_user)

        url = reverse("get-ticket", kwargs={'event_id':self.event1.id})
        response = self.client.post(url)
        ticket = Ticket.objects.filter(event=self.event1, attendee=attendee, is_used=False).exists()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ticket)

    def test_update_event_details(self):
        data = {
            "name": "Gaming Tournament",
            "time": timezone.now(),
            "venue": "New Venue",
            "ticket_price": "600.00",
            "organizer": self.organizer.pk
        }

        url = reverse("event-detail", kwargs={'event_id':self.event1.id})
        response = self.client.put(url, data)
        
        # Refresh event from db
        self.event1.refresh_from_db()

        self.assertEqual(self.event1.venue, 'New Venue')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_event(self):
        url = reverse("event-detail", kwargs={'event_id':self.event1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)








class TicketTestCase(EventsTestCase):
    def test_get_all_tickets(self):
        attendee_user = get_user_model().objects.create_user(
            email='attendee@example.com',
            password='password',
            user_type='attendee'
        )
        self.client.force_login(attendee_user)
        url = reverse("ticket")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_specific_ticket(self):
        attendee_user = get_user_model().objects.create_user(
            email='attendee@example.com',
            password='password',
            user_type='attendee'
        )
        self.client.force_login(attendee_user)
        attendee = Attendee.objects.get(user=attendee_user)
        ticket = Ticket.objects.create(event=self.event1, attendee=attendee)
        url = reverse("ticket-detail", kwargs={'ticket_id':ticket.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
