from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import RegisterForm


class RegisterView(View):
    template_name = "users/register.html"
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="quotes:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Вітаємо! {username}.Акаунт успішно створено")
            return redirect(to="users:login")
        return render(request, self.template_name, {"form": form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    success_message = "На вашу електронну адресу надіслано листа з інструкціями для відновлення паролю."
    subject_template_name = "users/password_reset_subject.txt"
