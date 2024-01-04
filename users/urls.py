from django.urls import path
from . import views
from rest_framework_simplejwt.views import  TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', views.RegisterUser, name='register'),
    path('verify_email/', views.verify_email, name='verify-email'),
    path('verify/', views.verify, name='verify'),
    path('organizer/', views.organizer_profile, name='organizer-profile'),
    path('attendee/', views.attendee_profile, name='attendee-profile'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
