from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models import Attendee, Organizer


from users.serializers import AttendeeSerializer, OrganizerSerializer, UserRegisterSerializer
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
def organzier_profile(request):
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
