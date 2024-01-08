from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from core.models import Event, Ticket

from users.models import Attendee, Organizer


class IsOrganizerPermission(BasePermission):
    '''This permission allows only Organizers make post reuest to create an event'''
    message = "You're not an Event Organizer"
    def has_permission(self, request, view):

        # Allos if the user is authenticated and reuest is not a post reuest
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True

        # Allos the user making post request is an organizer.
        user = request.user.id
        try:
            organizer = Organizer.objects.get(user=user)
        except Organizer.DoesNotExist:
            return False
        return request.user and request.user.is_authenticated and organizer


class GetEventTicketsPermission(BasePermission):
    '''Only event creator can see the tickets gotten for his event'''

    message = 'You did not create this event'
    def has_permission(self, request, view):
        from core.views import event_tickets
        if event_tickets:
            event = get_object_or_404(Event, id=view.kwargs.get('event_id'))
            organizer = event.organizer
            try:
                request_org = Organizer.objects.get(user=request.user.id)
            except Organizer.DoesNotExist:
                return False
        return request.user and request.user.is_authenticated and organizer == request_org


class GetTicketPermission(BasePermission):
    '''Allos only attendees to be able to get a ticket to an event'''

    def has_permission(self, request, view):
        # Allos access to vie only if the user is an attendee
        user = request.user.id
        
        if user is None:
            self.message = "User is not logged in"
            return False
        
        if request.user.user_type == 'organizer':
            self.message = "Organizer does not have access"
            return False
        
        if not request.user.is_verified:
            self.message =  "Your email is unverified"
            return False
        
        try:
            attendee = get_object_or_404(Attendee, user=user)
        except Attendee.DoesNotExist:
            self.message = "Attendee User does not exist"
            return False
        
        # Check if attendee has tickets to this event
        from core.views import get_ticket
        if get_ticket:
            event = Event.objects.get(id=view.kwargs.get('event_id'))

            if event.tickets.filter(attendee=attendee.id).exists():
                self.message = "You already have a ticket to this event"
                return False

        return request.user and request.user.is_authenticated and attendee


class EventDetailPermission(BasePermission):
    '''This permission allows only Organizers make post reuest to create an event'''
    message = "You're not an Event Organizer"
    
    def has_permission(self, request, view):
        # Permission to allo access to view
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Permission to allo access to object methods (PUT,DELETE)
        from core.views import event_detail
        if event_detail:
            event = Event.objects.get(id=view.kwargs.get('event_id'))
            organizer = event.organizer
            try:
                request_org = Organizer.objects.get(user=request.user.id)
            except Organizer.DoesNotExist:
                return False
        return request.user and request.user.is_authenticated and organizer == request_org


class IsAttendeePermission(BasePermission):
    '''This permission allows only attendee make post reuest to get ticket to an event'''
    def has_permission(self, request, view):
        # Allos the user making post request is an organizer.
        user = request.user.id
        try:
            attendee = Attendee.objects.get(user=user)
        except Attendee.DoesNotExist:
            return False
        return request.user and request.user.is_authenticated and attendee


class IsTicketOnerPermission(BasePermission):
    '''This permission allows only attendee vie ticket details'''
    def has_permission(self, request, view):
        # Allos the user making post request is an organizer.
        ticket = get_object_or_404(Ticket, id=view.kwargs.get('ticket_id'))
        attendee = ticket.attendee
        try:
            request_att = Attendee.objects.get(user=request.user.id)
        except Attendee.DoesNotExist:
            return False
        return request.user and request.user.is_authenticated and attendee == request_att
