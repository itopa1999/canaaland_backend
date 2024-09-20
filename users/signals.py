from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from secretary.models import Income
from .models import (
    User,
    District
)

@receiver(post_save, sender=District)
def Create_District_Account_Balance(sender, instance, created, **kwargs):
    if created:
        Income.objects.create(
            district = instance,
            income = 0
        )
        