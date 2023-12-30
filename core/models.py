import uuid
from django.db import models
from users.models import Attendee, Organizer

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length = 100)
    time = models.DateTimeField()
    venue = models.CharField(max_length=100)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE,related_name='events')

    def __str__(self):
        return self.name


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name='tickets') 
    ticket_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False) 



    def __str__(self):
            return f'Ticket {self.ticket_number} for {self.event.name} by {self.attendee.user.email}'