import uuid
from django.db import models
from users.models import Attendee, Organizer

# Create your models here.

class Event(models.Model):
    EXPIRED = 'expired'
    AVAILABLE = 'available'

    STATUS = [
        (EXPIRED, ('expired')),
        (AVAILABLE, ('available'))
    ]

    name = models.CharField(max_length = 100)
    time = models.DateTimeField()
    venue = models.CharField(max_length=100)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='events')
    status = models.CharField(max_length=50, choices=STATUS, default=AVAILABLE)

    def __str__(self):
        return f'{self.name} {self.id}'
    

class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket_type")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField(null=True, blank=True)
    tickets_available = models.PositiveIntegerField(default=0)

    def __str__(self): 
        return f'{self.id} {self.event.name} {self.name}  Ticket'


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name='tickets') 
    ticket_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False) 

    def __str__(self):
            return f'{self.id} {self.ticket_type} to {self.event.name} for {self.attendee.user.email}'