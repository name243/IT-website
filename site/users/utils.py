from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_confirmation_email(user, confirmation):
    """Отправка письма с подтверждением"""
    subject = 'Подтверждение email адреса'

    # HTML версия письма
    html_message = render_to_string('users/email_confirmation.html', {
        'user': user,
        'confirmation': confirmation,
        'domain': '127.0.0.1:8000',  # Замените на ваш домен
    })

    # Текстовая версия письма
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_welcome_email(user):
    """Отправка приветственного письма после подтверждения"""
    subject = 'Добро пожаловать!'

    html_message = render_to_string('users/welcome_email.html', {
        'user': user,
    })

    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )