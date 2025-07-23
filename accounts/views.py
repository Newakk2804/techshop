from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm, CustomUserCreationForm


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
