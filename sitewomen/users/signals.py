# users/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, EmailConfirmation


@receiver(post_save, sender=User)
def create_user_objects(sender, instance, created, **kwargs):
    """Создает все связанные объекты при создании пользователя"""
    if created:
        # Создаем профиль (если его еще нет)
        if not hasattr(instance, 'profile'):
            Profile.objects.get_or_create(user=instance)

        # Создаем подтверждение email (если его еще нет)
        if not hasattr(instance, 'emailconfirmation'):
            EmailConfirmation.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()