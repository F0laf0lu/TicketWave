from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Event, Ticket
from users.models import Attendee, Organizer

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ['organizer']
    # def create(self, validated_data):
    #     user = self.context.get('user')
    #     organizer = Organizer.objects.get(user=user)
    #     validated_data['organizer'] = organizer.id
    #     return Event.objects.create(**validated_data)


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