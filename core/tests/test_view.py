from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model 
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from users.models import Organizer, Attendee
from core.models import Event, Ticket, TicketType

class EventsTestCase(APITestCase):
    def setUp(self):
        self.organizer_user = get_user_model().objects.create_user(
            email='organizer@example.com',
            password='password',
            user_type='organizer',
            is_verified = True
        )

        self.organizer = Organizer.objects.get(user=self.organizer_user)

        # Login User
        self.client.force_authenticate(user=self.organizer_user)

        # Create some events for testing
        self.event1 = Event.objects.create(
            name='Event 1', 
            time = timezone.now(),
            venue='Venue 1',
            organizer = self.organizer,
            status = 'available'
        )
        
        self.event2 = Event.objects.create(
            name ='Event 2', 
            time = timezone.now(),
            venue='Venue 2',
            organizer = self.organizer,
            status = 'available'
        )
        
        #Create TicketTypes
        self.ticket_type1 = TicketType.objects.create(
            event = self.event1, 
            name = 'Vip Tickets',
            price = 700,
            tickets_available = 1
        )

        self.ticket_type2 = TicketType.objects.create(
            event = self.event2, 
            name = 'Vip Tickets',    
            price = 700,
            tickets_available = 0
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
            "ticket_type": [
                {
                    "name": "Slots",
                    "price": "500.00",
                    "details": ""
                }
            ],
            "organizer": self.organizer.pk
        }

        url = reverse("events")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_event_details(self):
        url = reverse("event-detail", kwargs={'event_id':self.event1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_ticket_for_event(self):
        data = {
            "ticket_type" : self.ticket_type1.pk
        }

        attendee_user = get_user_model().objects.create_user(
            email='attendee@example.com',
            password='password',
            user_type='attendee',
            is_verified = True
        )

        self.client.force_authenticate(attendee_user)

        attendee = Attendee.objects.get(user=attendee_user)

        url = reverse("get-ticket", kwargs={'event_id':self.event1.id})

        response = self.client.post(url, data, format='json')
        ticket = Ticket.objects.filter(event=self.event1, attendee=attendee, is_used=False).exists()


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ticket)


    def test_update_event_details(self):
        data = {
            "name": "Gaming Tournament",
            "time": timezone.now(),
            "venue": "New Venue",
            "ticket_type": [
                {
                    "name": "Slots",
                    "price": "500.00",
                    "details": ""
                }
            ],
            "organizer": self.organizer.pk
        }

        url = reverse("event-detail", kwargs={'event_id':self.event1.pk})
        response = self.client.patch(url, data, format='json')

        # Refresh event from db
        self.event1.refresh_from_db()

        self.assertEqual(self.event1.venue, 'New Venue')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_event(self):
        url = reverse("event-detail", kwargs={'event_id':self.event1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)











class TicketTestCase(APITestCase):
    def setUp(self):
        self.organizer_user = get_user_model().objects.create_user(
            email='organizer@example.com',
            password='password',
            user_type='organizer',
            is_verified = True
        )
        self.organizer = Organizer.objects.get(user=self.organizer_user)
        self.event1 = Event.objects.create(
            name='Event 1', 
            time = timezone.now(),
            venue='Venue 1',
            organizer = self.organizer,
            status = 'available'
        )
        #Create TicketTypes
        self.ticket_type1 = TicketType.objects.create(
            event = self.event1, 
            name = 'Vip Tickets',
            price = 700,
            tickets_available = 1
        )
        self.attendee_user = get_user_model().objects.create_user(
                    email='attendee@example.com',
                    password='password',
                    user_type='attendee',
                    is_verified = True
                )
        self.client.force_authenticate(self.attendee_user)
        



    def test_get_all_attendee_tickets(self):
        url = reverse("ticket")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_attendee_ticket(self):
        attendee = Attendee.objects.get(user=self.attendee_user)

        ticket = Ticket.objects.create(event=self.event1, ticket_type=self.ticket_type1, attendee=attendee)
        url = reverse("ticket-detail", kwargs={'ticket_id':ticket.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def ticket_unavailable(self):
        data = {
            "ticket_type" : self.ticket_type2.pk
        }

        attendee = Attendee.objects.get(user=self.attendee_user)

        url = reverse("get-ticket", kwargs={'event_id':self.event1.id})

        response = self.client.post(url, data, format='json')
        ticket = Ticket.objects.filter(event=self.event1, attendee=attendee, is_used=False).exists()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(ticket)
