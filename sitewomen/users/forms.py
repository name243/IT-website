from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ваше имя',
            'autocomplete': 'given-name'
        })
    )

    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ваш email',
            'autocomplete': 'email'
        })
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Придумайте пароль',
            'autocomplete': 'new-password'
        })
    )

    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Повторите пароль',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2')

    def clean_first_name(self):
        """Проверка имени"""
        first_name = self.cleaned_data.get('first_name')

        if not first_name:
            raise ValidationError("Имя обязательно для заполнения")

        if len(first_name) < 2:
            raise ValidationError("Имя должно содержать не менее 2 символов")

        if not first_name.isalpha():
            raise ValidationError("Имя должно содержать только буквы")

        return first_name

    def clean_email(self):
        """Проверка email и уникальности username"""
        email = self.cleaned_data.get('email')

        if not email:
            raise ValidationError("Email обязателен для заполнения")

        # Проверяем, существует ли пользователь с таким email
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")

        # Проверяем, существует ли пользователь с таким username (email)
        if User.objects.filter(username=email).exists():
            raise ValidationError("Пользователь с таким email уже зарегистрирован")

        return email

    def clean_password1(self):
        """Дополнительная проверка пароля"""
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise ValidationError("Пароль должен содержать не менее 8 символов")

        if not re.search(r'[A-Z]', password1):
            raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву")

        if not re.search(r'[a-z]', password1):
            raise ValidationError("Пароль должен содержать хотя бы одну строчную букву")

        if not re.search(r'[0-9]', password1):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру")

        return password1

    def clean(self):
        """Общая проверка формы"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.username = self.cleaned_data['email']  # Используем email как username
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Создаем связанные объекты через get_or_create чтобы избежать дубликатов
            from .models import Profile, EmailConfirmation
            Profile.objects.get_or_create(user=user)
            EmailConfirmation.objects.get_or_create(user=user)

        return user