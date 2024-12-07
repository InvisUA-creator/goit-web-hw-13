from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from . import views
from .forms import LoginForm

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"
    ),
    path("reset-password/", views.ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            succes_url="/users/reset-password/complite/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complite/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
