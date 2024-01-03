from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated



from users.utils import send_code_to_user
from users.models import Attendee, Organizer
from users.serializers import AttendeeSerializer, EmailSerializer, OrganizerSerializer, UserRegisterSerializer
from users.permissions import IsNotAuthenticated

# Create your views here.

@api_view(['POST'])
@permission_classes([IsNotAuthenticated])
def RegisterUser(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': f'Hi {serializer.data["email"]} Thanks for signing up'
            }, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def organizer_profile(request):
    user = get_object_or_404(Organizer, user=request.user)
    if request.method == 'GET':
        serializer = OrganizerSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = OrganizerSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def attendee_profile(request):
    user = get_object_or_404(Attendee, user=request.user)
    if request.method == 'GET':
        serializer = AttendeeSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = AttendeeSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Permission - Only unverified users can access this
@api_view(['POST'])
def verify_email(request):
    email = request.user.email
    if request.method == 'POST':
        serializer = EmailSerializer(data= {'email':email})
        if serializer.is_valid():
            # Send otp to email
            send_code_to_user()
            print(serializer.validated_data)
            return Response(
                {
                    "message": "Email verified successfully.", 
                    "email":serializer.data['email']
                }, 
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)