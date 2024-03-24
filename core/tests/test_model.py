from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import Organizer, Attendee
from core.models import Event, Ticket, TicketType
import os
from django import setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketwave.testsettings')
setup()
# Create your tests here.

class EventModelTests(TestCase):
    def setUp(self):
        self.organizer_user = get_user_model().objects.create_user(
            email='organizer@example.com',
            password='password',
            user_type='organizer'
        )
        self.organizer = Organizer.objects.get(user=self.organizer_user)

    def test_event_creation(self):
        event = Event.objects.create(
            name='Test Event',
            time=timezone.now(),
            venue='Test Venue',
            organizer=self.organizer
        )


class TicketModelTest(TestCase):
    def setUp(self):
        self.organizer_user = get_user_model().objects.create_user(
            email='organizer@example.com',
            password='password',
            user_type='organizer'
        )
        self.organizer = Organizer.objects.get(user=self.organizer_user)

        self.attendee_user = get_user_model().objects.create_user(
            email='attendee@example.com',
            password='password',
            user_type='attendee'
        )
        self.attendee = Attendee.objects.get(user=self.attendee_user)

        self.event = Event.objects.create(
            name='Test Event',
            time=timezone.now(),
            venue='Test Venue',
            organizer=self.organizer
        )

        self.ticket_type = TicketType.objects.create(
            event = self.event,
            name = 'Vip Tickets',
            price = 700
        )


    def test_ticket_creation(self):
        ticket = Ticket.objects.create(
            event=self.event,
            ticket_type = self.ticket_type,
            attendee=self.attendee,
            ticket_number='123e4567-e89b-12d3-a456-426614174001'
        )
        self.assertEqual(ticket.event, self.event)
        self.assertEqual(ticket.attendee, self.attendee)
        self.assertFalse(ticket.is_used)

