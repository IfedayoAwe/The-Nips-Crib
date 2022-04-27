from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from .models import Profile
from django.conf import settings
from rest_framework.authtoken.models import Token

from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="NipsCrib.com"),
        # message:
        email_plaintext_message,
        # from:
        "nipscrib@gmail.com",
        # to:
        [reset_password_token.user.email]
    )