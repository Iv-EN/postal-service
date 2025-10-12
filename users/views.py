from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    TemplateView,
    UpdateView,
)

from services.mixins import UserIsNotAuthenticated
from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    PasswordResetForm,
    UserForgotPasswordForm,
    UserSetNewPasswordForm,
)
from .managers import UserManager
from .models import CustomUser


class RegisterView(UserIsNotAuthenticated, CreateView):
    """Представление для регистрации на сайте."""

    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def get_context_data(self, **kwargs):
        """Передает контекстные данные."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация на сайте"
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy(
            "users:confirm_email",
            kwargs={
                "uid64": uid,
                "token": token,
            },
        )
        current_site = "127.0.0.1:8000"
        send_mail(
            "Подтвердите свой электронный адрес",
            f"Перейдите по ссылке: http://{current_site}{activation_url}, что бы подтвердить.",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return redirect("users:email_confirmation_sent")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования профиля пользователя."""

    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "users/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = (
            f"Редактирование профиля пользователя: {self.object.username}"
        )
        return context

    def form_valid(self, form):
        with transaction.atomic():
            form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "users:profile_detail", kwargs={"id": self.object.id}
        )


class ConfirmEmailView(View):
    """Представление для подтверждения email."""

    def get(self, request, uid64, token):
        """Проверяет токен и активирует пользователя."""
        try:
            uid = urlsafe_base64_decode(uid64)
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(
            user, token
        ):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("users:email_confirmed")
        return redirect("users:email_confirmation_failed")


class EmailConfirmationSentView(TemplateView):
    template_name = "users/confirmation_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо активации отправлено"
        return context


class EmailConfirmedView(TemplateView):
    template_name = "users/email_confirmed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ваш электронный адрес активирован"
        return context


class EmailConfirmationFailedView(TemplateView):
    """Представление для отображения страницы ошибки активации."""

    template_name = "users/email_confirmation_failed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ошибка активации"
        return context


class ProfileDetailView(DetailView):
    """Представление для просмотра профиля."""

    model = CustomUser
    context_object_name = "profile"
    template_name = "users/profile_detail.html"

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.kwargs["id"])


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """Представление по сбросу пароля по почте."""

    form_class = UserForgotPasswordForm
    template_name = "users/user_password_reset.html"
    success_url = reverse_lazy("mailing:home")
    success_message = (
        "Письмо с инструкцией по восстановлению пароля "
        "будет отправлено на указанный email"
    )
    subject_template_name = "users/password_subject_reset_mail.txt"
    email_template_name = "users/password_reset_mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Запрос на восстановление пароля"
        return context


class UserPasswordResetConfirmView(
    SuccessMessageMixin, PasswordResetConfirmView
):
    """Представление установки нового пароля."""

    form_class = UserSetNewPasswordForm
    template_name = "users/user_password_set_new.html"
    success_url = reverse_lazy("mailing:home")
    success_message = "Пароль успешно изменен. Можете авторизоваться на сайте."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Установить новый пароль"
        return context


class UserManagementViews(LoginRequiredMixin, View):
    """Представление для управления пользователями."""

    model = CustomUser
    template_name = "users/user_management.html"

    def get(self, request, *args, **kwargs):
        user_manager = UserManager(request.user)
        users = user_manager.list_users()
        is_manager_group = request.user.groups.filter(
            name="Менеджеры"
        ).exists()
        return render(
            request,
            self.template_name,
            {
                "users": users,
                "is_manager_group": is_manager_group,
            },
        )

    def post(self, request, *args, **kwargs):
        user_manager = UserManager(request.user)
        user_id = request.POST.get("user_id")
        user_manager.block_user(user_id)
        return self.get(request, *args, **kwargs)
