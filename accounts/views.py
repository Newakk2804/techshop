from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomPasswordResetForm, CustomPasswordConfirmFrom


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("store:index")
    else:
        form = CustomUserCreationForm()

    context = {"form": form}
    return render(request, "accounts/register.html", context)


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if not form.cleaned_data.get("remember_me"):
                request.session.set_expiry(0)

            return redirect("store:index")
    else:
        form = CustomAuthenticationForm()

    context = {"form": form}
    return render(request, "accounts/login.html", context)


@login_required
def logout_view(request):
    logout(request)
    return redirect("store:index")


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "accounts/reset_pwd/password_reset_form.html"
    success_url = reverse_lazy("accounts:password_reset_done")

class CustomPassowrdResetDoneView(PasswordResetDoneView):
    template_name = "accounts/reset_pwd/password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordConfirmFrom
    template_name = "accounts/reset_pwd/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/reset_pwd/password_reset_complete.html"