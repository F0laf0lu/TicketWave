from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Event, Ticket, TicketType
from users.models import Attendee, Organizer


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['name', 'price', 'details']
        read_only_fields = ['event']

class EventSerializer(serializers.ModelSerializer):
    ticket_type = TicketTypeSerializer(many=True)
    
    class Meta:
        model = Event
        fields = ['name', 'time', 'venue', 'organizer', 'ticket_type']
        read_only_fields = ['organizer']

    def create(self, validated_data):
        ticket_types_data = validated_data.pop('ticket_type', [])  
        event = Event.objects.create(**validated_data)

        for ticket_type_data in ticket_types_data:
            TicketType.objects.create(event=event, **ticket_type_data)

        return event

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ['attendee', 'event']

    def create(self, validated_data):
        event_id = self.context.get('event')
        user = self.context.get('user')
        attendee = Attendee.objects.get(user=user)
        event = get_object_or_404(Event, id=event_id)
        
        validated_data['event'] = event
        validated_data['attendee'] = attendee
        return Ticket.objects.create(**validated_data)