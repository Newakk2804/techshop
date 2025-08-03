from django.urls import path
from .views import login_view, register_view, logout_view
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path(
        "password-reset/",
        views.CustomPasswordResetView.as_view(
            template_name="accounts/reset_pwd/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        views.CustomPassowrdResetDoneView.as_view(
            template_name="accounts/reset_pwd/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(
            template_name="accounts/reset_pwd/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.CustomPasswordResetCompleteView.as_view(
            template_name="accounts/reset_pwd/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
