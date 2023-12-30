from django.db import models
from django.contrib.auth.models import AbstractUser
from . manager import CustomUserManager
from django.contrib.auth import get_user_model

# Create your models here.
class CustomUser(AbstractUser):

    ORGANIZER = 'organizer'
    ATTENDEE = 'attendee'

    USER_TYPE = [
        (ORGANIZER, ('Organizer')),
        (ATTENDEE, ('Attendee'))
    ]

    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Organizer(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length = 100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    contact_phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.email

class Attendee(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    contact_phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.email 

