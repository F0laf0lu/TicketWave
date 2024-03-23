from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import Organizer, Attendee

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
            raise serializers.ValidationError("Your passwords no match oga")
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        user_type =  validated_data['user_type']
        password = validated_data['password']
        return get_user_model().objects.create_user(email=email, user_type=user_type, password=password)

class OtpCodeSerializer(serializers.Serializer):
    otpcode = serializers.CharField(max_length=200)


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ["user","name", "website", "bio", "contact_phone"]
        read_only_fields = ['user']


class AttendeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendee
        fields = ["user", "date_of_birth", "contact_phone"]
        read_only_fields = ['user']


class UserSerializer(serializers.ModelSerializer):
    attendee = AttendeeSerializer(required=False)
    organizer = OrganizerSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = [ "id", 'email', "user_type", "attendee", "organizer"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        attendee_exists = hasattr(instance, 'attendee') and instance.attendee is not None
        organizer_exists = hasattr(instance, 'organizer') and instance.organizer is not None
        if attendee_exists:
            representation.pop('organizer', None)
        elif organizer_exists:
            representation.pop('attendee', None)
        return representation

# Update User Serializers
class AttendeeUpdateSerializer(serializers.ModelSerializer):
    attendee = AttendeeSerializer(required=False)
    class Meta:
        model = get_user_model()
        fields = ["id", 'email', "user_type", "attendee"]
        read_only_fields = ['user_type', "email"]

    def update(self, instance, validated_data):
        print(validated_data['attendee'])
        data = validated_data['attendee']

        att_user = Attendee.objects.get(user__email=instance.attendee)
        att_user.date_of_birth = data.get('date_of_birth', att_user.date_of_birth)
        att_user.contact_phone = data.get('contact_phone', att_user.contact_phone)
        att_user.save()
        return instance




class OrganizerUpdateSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(required=False)
    class Meta:
        model = get_user_model()
        fields = ["id", 'email', "user_type", "organizer"]
        read_only_fields = ['user_type', "email"]

    def update(self, instance, validated_data):
        print(validated_data['organizer'])
        data = validated_data['organizer']

        org_user = Organizer.objects.get(user__email=instance.organizer)
        org_user.name = data.get('name', org_user.name)
        org_user.website = data.get('website', org_user.website)
        org_user.bio = data.get('bio', org_user.bio)
        org_user.contact_phone = data.get('contact_phone', org_user.contact_phone)
        org_user.save()
        return instance

