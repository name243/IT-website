from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=24)

    def __str__(self):
        return f"Confirmation for {self.user.email}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True)
    bio = models.TextField('О себе', blank=True)

    def __str__(self):
        return f'Профиль {self.user.username}'


# Сигналы для автоматического создания объектов
@receiver(post_save, sender=User)
def create_user_objects(sender, instance, created, **kwargs):
    """Создает EmailConfirmation и Profile при создании пользователя"""
    if created:
        # Создаем подтверждение email
        EmailConfirmation.objects.create(user=instance)

        # Создаем профиль
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()