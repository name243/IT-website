from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .models import EmailConfirmation, Profile
from .utils import send_confirmation_email, send_welcome_email


# users/views.py
# users/views.py
def register_view(request):
    """Обработка формы регистрации с отправкой подтверждения"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False  # Делаем неактивным до подтверждения email
                user.save()

                # Отправляем письмо с подтверждением
                from .models import EmailConfirmation
                from .utils import send_confirmation_email

                confirmation = EmailConfirmation.objects.get(user=user)
                send_confirmation_email(user, confirmation)

                messages.success(request, 'Регистрация почти завершена! Проверьте вашу почту для подтверждения email.')
                return redirect('login')

            except IntegrityError as e:
                messages.error(request, 'Ошибка при создании пользователя. Возможно, такой email уже существует.')
                return redirect('register')

        else:
            # Показываем ошибки формы пользователю
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})
def confirm_email_view(request, token):
    """Подтверждение email адреса"""
    try:
        confirmation = get_object_or_404(EmailConfirmation, token=token)

        if confirmation.is_expired():
            messages.error(request, 'Ссылка подтверждения истекла. Запросите новую.')
            return redirect('register')

        if confirmation.confirmed:
            messages.info(request, 'Email уже подтвержден.')
            return redirect('login')

        # Подтверждаем email
        confirmation.confirmed = True
        confirmation.save()

        # Активируем пользователя
        user = confirmation.user
        user.is_active = True
        user.save()

        # Отправляем приветственное письмо
        send_welcome_email(user)

        messages.success(request, 'Email успешно подтвержден! Теперь вы можете войти.')
        return redirect('login')

    except Exception:
        messages.error(request, 'Ошибка подтверждения email.')
        return redirect('register')


def resend_confirmation_view(request):
    """Повторная отправка подтверждения"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            confirmation, created = EmailConfirmation.objects.get_or_create(user=user)

            if confirmation.confirmed:
                messages.info(request, 'Email уже подтвержден.')
            else:
                send_confirmation_email(user, confirmation)
                messages.success(request, 'Письмо с подтверждением отправлено! Проверьте вашу почту.')

            return redirect('login')

        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким email не найден.')

    return render(request, 'users/resend_confirmation.html')


def login_view(request):
    """Обработка формы входа"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                # Проверяем, подтвержден ли email
                try:
                    confirmation = EmailConfirmation.objects.get(user=user)
                    if not confirmation.confirmed:
                        messages.error(request, 'Пожалуйста, подтвердите ваш email перед входом.')
                        return redirect('login')
                except EmailConfirmation.DoesNotExist:
                    # Если нет записи подтверждения, создаем ее
                    EmailConfirmation.objects.create(user=user)
                    messages.error(request, 'Пожалуйста, подтвердите ваш email перед входом.')
                    return redirect('login')

                login(request, user)
                welcome_name = user.first_name if user.first_name else user.username
                messages.success(request, f'Добро пожаловать, {welcome_name}!')
                return redirect('profile')
        else:
            messages.error(request, 'Неверные учетные данные.')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def profile_view(request):
    """Личный кабинет пользователя"""
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def settings_view(request):
    """Настройки пользователя"""
    return render(request, 'users/setting.html', {'user': request.user})


@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    """Список пользователей для админа"""
    users = User.objects.all()
    return render(request, 'admin/user_list.html', {'users': users})


# users/views.py
# users/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile


@login_required
def settings_view(request):
    if request.method == 'POST':
        # Определяем, какая форма была отправлена
        if 'save_profile' in request.POST:
            return save_profile(request)
        elif 'form_type' in request.POST and request.POST['form_type'] == 'change_password':
            return change_password(request)

    return render(request, 'users/setting.html', {'user': request.user})


def save_profile(request):
    """Сохраняет данные профиля"""
    try:
        # Обновляем основные данные пользователя
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.save()

        # Получаем или создаем профиль
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)

        # Обновляем профиль
        profile.phone = request.POST.get('phone', '')
        profile.bio = request.POST.get('bio', '')
        profile.save()

        messages.success(request, 'Данные профиля успешно сохранены!')
    except Exception as e:
        messages.error(request, f'Ошибка сохранения профиля: {str(e)}')

    return redirect('settings')


def change_password(request):
    """Изменяет пароль"""
    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    # Проверяем, что текущий пароль верный
    if not request.user.check_password(current_password):
        messages.error(request, 'Текущий пароль неверный')
        return redirect('settings')

    # Проверяем, что новый пароль и подтверждение совпадают
    if new_password != confirm_password:
        messages.error(request, 'Новые пароли не совпадают')
        return redirect('settings')

    # Проверяем длину пароля
    if len(new_password) < 8:
        messages.error(request, 'Пароль должен содержать не менее 8 символов')
        return redirect('settings')

    # Меняем пароль
    try:
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Важно: обновляем сессию
        messages.success(request, 'Пароль успешно изменен!')
    except Exception as e:
        messages.error(request, f'Ошибка при изменении пароля: {str(e)}')

    return redirect('settings')