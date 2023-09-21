"""This module contain definition of different signals"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import User, UserProfile, Invite


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal for creating a profile with user"""
    if created:
        Invite.objects.filter(email=instance.email).update(invitee=instance)
        UserProfile.objects.create(user=instance)
