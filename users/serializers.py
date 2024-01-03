from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import Organizer, Attendee

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email']

class UserRegisterSerializer(serializers.ModelSerializer):

    ORGANIZER = 'organizer'
    ATTENDEE = 'attendee'

    USER_TYPE = [
        (ORGANIZER, ('Organizer')),
        (ATTENDEE, ('Attendee'))
    ]

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    user_type = serializers.ChoiceField(choices=USER_TYPE)

    class Meta:
        model = get_user_model()
        fields = ['email', 'user_type', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2 :
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        user_type =  validated_data['user_type']
        password = validated_data['password']
        return get_user_model().objects.create_user(email=email, user_type=user_type, password=password)
    

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ["name", "website", "bio", "contact_phone"]

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ["date_of_birth", "contact_phone"]


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()