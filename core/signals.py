from django.dispatch import receiver
from django.db.models.signals import post_save

from . models import Event, TicketType

@receiver(post_save, sender=TicketType)
def update_event_status(sender, instance, created, **kwargs):
    event_id = instance.event.id
    event = Event.objects.get(pk=event_id)
    
    ticket_expired = all(ticket_type.tickets_available == 0 for ticket_type in event.ticket_type.all())

    if ticket_expired:
        event.status = 'expired'    
    else:
        event.status = 'available'
    event.save()
