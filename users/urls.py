from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/',  views.RegisterUserView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify_email/', views.verify_email, name='verify-email'),
    path('verifycode/', views.VerifyView.as_view(), name='verify_code'),
    path('profile/<int:pk>', views.UsersProfileView.as_view(), name='user-profile'),
]
