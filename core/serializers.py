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
    organizer = serializers.StringRelatedField()

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

    def update(self, instance, validated_data):
        ticket_types_data = validated_data.pop('ticket_type', [])

        instance.name = validated_data.get('name', instance.name)
        instance.time = validated_data.get('time', instance.time)
        instance.venue = validated_data.get('venue', instance.venue)
        instance.save()
        
        # Get all ticket_types for an event
        tickets = TicketType.objects.filter(event=instance.pk)
        ids = [i.pk for i in tickets]
        updated_ids = []
        for ticket_type in ticket_types_data:
            ticket_type_name = ticket_type.get('name')

            try:
                ticket_type_instance = TicketType.objects.get(event=instance, name=ticket_type_name)
                ticket_type_instance.name = ticket_type.get('name',ticket_type_instance.name)
                ticket_type_instance.price = ticket_type.get('price',ticket_type_instance.price)
                ticket_type_instance.details = ticket_type.get('details',ticket_type_instance.details)
                ticket_type_instance.save()
                updated_ids.append(ticket_type_instance.id)

            except TicketType.DoesNotExist:
                ticket_type_instance = TicketType.objects.create(event=instance, **ticket_type)
                updated_ids.append(ticket_type_instance.id)
            
        for ticket_id in ids:   
            if ticket_id not in updated_ids:
                TicketType.objects.get(id=ticket_id).delete()
        
        return instance

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ['attendee', 'event']


    def validate(self, attrs):
        ticket_type_id = attrs.get('ticket_type')
        event_id = self.context.get('event')

        #get events
        try: 
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise serializers.ValidationError({'event':'Event Not Found'})
        
        #get ticket_type for event
        try:
            ticket_type = TicketType.objects.get(id=ticket_type_id.id, event=event)
        except TicketType.DoesNotExist:
            raise serializers.ValidationError({'ticket type': 'Invalid ticket type obj'})
        
        return attrs

    def create(self, validated_data):
        event_id = self.context.get('event')
        user = self.context.get('user')
        attendee = Attendee.objects.get(user=user)
        event = get_object_or_404(Event, id=event_id)

        validated_data['event'] = event
        validated_data['attendee'] = attendee
        return Ticket.objects.create(**validated_data)