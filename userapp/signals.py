from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Profile
from django.conf import settings
from django.core.mail import send_mail

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, *args, **kwargs):
    if created:
        user = instance
        Profile.objects.create(user=user)

        subject, message = 'Welcome to DevProject', 'Welcome to DevProject, we are glad that you are here.'
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )
    else:
        print('Opps! instance already present.')

