from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    ConfirmEmailView,
    EmailConfirmationFailedView,
    EmailConfirmationSentView,
    EmailConfirmedView,
    ProfileDetailView,
    ProfileUpdateView,
    RegisterView,
    UserForgotPasswordView,
    UserManagementViews,
    UserPasswordResetConfirmView,
)

app_name = "users"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "confirm-email/<str:uid64>/<str:token>/",
        ConfirmEmailView.as_view(),
        name="confirm_email",
    ),
    path(
        "email-confirmation-sent/",
        EmailConfirmationSentView.as_view(),
        name="email_confirmation_sent",
    ),
    path(
        "email-confirmed/",
        EmailConfirmedView.as_view(),
        name="email_confirmed",
    ),
    path(
        "confirm-email-failed/",
        EmailConfirmationFailedView.as_view(),
        name="email_confirmation_failed",
    ),
    path("user/<int:id>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path(
        "password-reset/",
        UserForgotPasswordView.as_view(),
        name="password_reset",
    ),
    path(
        "set-new-password/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("management/", UserManagementViews.as_view(), name="user_management"),
]
