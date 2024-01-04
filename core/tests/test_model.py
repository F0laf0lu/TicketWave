from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import Organizer, Attendee
from core.models import Event, Ticket

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
            ticket_price=10.0,
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
            ticket_price=10.0,
            organizer=self.organizer
        )

    def test_ticket_creation(self):
        ticket = Ticket.objects.create(
            event=self.event,
            attendee=self.attendee,
            ticket_number='123e4567-e89b-12d3-a456-426614174001'
        )
        self.assertEqual(ticket.event, self.event)
        self.assertEqual(ticket.attendee, self.attendee)
        self.assertFalse(ticket.is_used)

