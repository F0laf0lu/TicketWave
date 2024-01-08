from django.shortcuts import get_object_or_404
from core.models import TicketType,Event


class TicketService:
    @staticmethod
    def purchase_ticket(ticket_type_id):
        ticket_type = get_object_or_404(TicketType, id=ticket_type_id)
        event_id = ticket_type.event.id
        event = Event.objects.get(pk=event_id)

        if ticket_type.tickets_available > 0:
            # Perform the purchase logic
            ticket_type.tickets_available -= 1
            ticket_type.save()
            if ticket_type.tickets_available == 0:
                event.status = 'expired'

            return True, 'Ticket purchased successfully'
        else:
            return False, 'Tickets are no longer on sale'