from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from . models import Organizer, Attendee

@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'Organizer':
            Organizer.objects.create(user=instance)
        elif instance.user_type == 'Attendee':
            Attendee.objects.create(user=instance)
