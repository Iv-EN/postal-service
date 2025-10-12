from django import forms
from django.contrib.auth.forms import (
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)

from mailing.forms import StyleFormMixin
from .models import CustomUser


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    """Форма создания нового пользователя."""

    phone_number = forms.CharField(
        max_length=12,
        required=False,
        help_text="Введите номер телефона (не обязательно).",
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "phone_number",
            "password1",
            "password2",
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError(
                "Номер телефона должен состоять только из цифр."
            )
        return phone_number


class CustomUserChangeForm(StyleFormMixin, forms.ModelForm):
    """Форма изменения информации о пользователе."""

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number", "avatar", "country")


class UserForgotPasswordForm(StyleFormMixin, PasswordResetForm):
    """Запрос на восстановление пароля."""

    pass


class UserSetNewPasswordForm(StyleFormMixin, SetPasswordForm):
    """Изменение пароля пользователя после подтверждения."""

    pass


class UserManagementForm(StyleFormMixin, forms.ModelForm):
    """Форма для просмотра и блокировки пользователей."""

    class Meta:
        model = CustomUser
        fields = ("username", "email", "is_active")
