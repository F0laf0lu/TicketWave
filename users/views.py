from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from users.utils import send_code_to_user
from users.models import Attendee, Organizer
from users.serializers import OtpCodeSerializer, UserSerializer, UserRegisterSerializer
from users.permissions import IsNotAuthenticated, IsUnverified, IsOwnerOrReadOnly
import pyotp

# Create your views here.

class RegisterUserView(CreateAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = UserRegisterSerializer

class UsersProfileView(RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_role'] = self.request.user.user_type
        print(context)
        return context

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404 as e:
            return Response({"Error": str(e)}, status=status.HTTP_404_NOT_FOUND)



# Permission - Only unverified users can access this
@api_view(['POST'])
@permission_classes([IsUnverified])
def verify_email(request):
    email = request.user.email
    if request.method == 'POST':
        # Send otp to user email
        send_code_to_user(email)
        return Response(
                {
                    "message": "OTP sent successfully to your email", 
                    "email":email
                }, 
                status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

class VerifyView(APIView):

    @swagger_auto_schema(
        request_body=OtpCodeSerializer,
        responses={
            200: openapi.Response('Email verification successful'),
            204: openapi.Response('User is already verified'),
            400: openapi.Response('Invalid OTP code')
        },
        operation_description="Verify user with OTP code"
    )

    def post(self, request):
        serializer = OtpCodeSerializer(data=request.data)
        if serializer.is_valid():
            otpcode = serializer.validated_data.get('otpcode')
            user = request.user

            i, secret_key = user.secret_key.split("-")
            hotp = pyotp.HOTP(secret_key)

            # Verify code
            if hotp.verify(otpcode, int(i)):

                # Verify user if code
                if not user.is_verified:
                    user.is_verified= True
                    user.save()

                    return Response({
                        'message':'Email verification successful'
                    }, status=status.HTTP_200_OK)
                return Response({'message': 'User is already verified'} , status=status.HTTP_204_NO_CONTENT)

        return Response({
                    'message': 'Invalid OTP code'
                },  status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsUnverified])
def verify(request):
    if request.method == 'POST':
        otpcode = request.data.get('otp')
        user = request.user

        i, secret_key = user.secret_key.split("-")
        hotp = pyotp.HOTP(secret_key)

        # Verify code
        if hotp.verify(otpcode, int(i)):

            # Verify user if code
            if not user.is_verified:
                user.is_verified= True
                user.save()

                return Response({
                    'message':'Email verification successful'
                }, status=status.HTTP_200_OK)
            return Response({'message': 'User is already verified'} , status=status.HTTP_204_NO_CONTENT)

        return Response({
                    'message': 'Invalid OTP code'
                },  status=status.HTTP_400_BAD_REQUEST)
