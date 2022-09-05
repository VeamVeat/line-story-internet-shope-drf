from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import File
from users.models import User, Profile, Wallet


@receiver(post_save, sender=User)
def create_profile_and_wallet(sender, instance, created, **kwargs):
    if created:
        file = File.objects.create(image='users/photo_profile/default.png')
        Profile.objects.create(user=instance, image=file)
        Wallet.objects.create(user=instance)
