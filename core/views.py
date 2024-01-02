from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from core.models import Event, Ticket
from users.models import Attendee, Organizer
from .serializers import EventSerializer, TicketSerializer
from .permissions import EventDetailPermission, IsOrganizerPermission, GetTicketPermission, GetEventTicketsPermission, IsAttendeePermission, IsTicketOnerPermission

# Create your views here.

user = get_user_model()

# Get all events
# create event 
@api_view(['GET', 'POST'])
@permission_classes([IsOrganizerPermission])
def events(request):
    if request.method == 'GET':
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        user = request.user.id
        organizer = Organizer.objects.get(user=user)
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['organizer'] = organizer
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Get a specific event
@api_view(['GET','PUT', 'DELETE'])
@permission_classes([EventDetailPermission])
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventSerializer(instance=event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# All tickets created or bought for an event
@api_view(['GET'])
@permission_classes([GetEventTicketsPermission])
def event_tickets(request, event_id):
    if request.method == 'GET':
        ticket = Ticket.objects.filter(event=event_id)
        serializer = TicketSerializer(ticket, many=True)
        return Response(serializer.data)

# get a ticket for an event
@api_view(["POST"])
@permission_classes([GetTicketPermission])
def get_ticket(request, event_id):
    if request.method == 'POST':
        context = {"event": event_id, 'user':request.user.id}
        serializer = TicketSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get all tickets
@api_view(['GET'])
@permission_classes([IsAttendeePermission])
def tickets(request):
    attendee = get_object_or_404(Attendee, user=request.user.id)
    if request.method == 'GET':
        ticket = attendee.tickets.all()
        serializer = TicketSerializer(ticket, many=True)
        return Response(serializer.data)

# Get ticket details
@api_view(['GET'])
@permission_classes([IsTicketOnerPermission])
def ticket_detail(request, ticket_id):
    attendee = get_object_or_404(Attendee, user=request.user.id)
    if request.method == 'GET':
        ticket  = get_object_or_404(Ticket, id=ticket_id)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)