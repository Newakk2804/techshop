from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.conf import settings
from accounts.models import CustomUser

from accounts.tasks import send_custom_email


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Электронная почта",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите ваш Email"}
        ),
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
        help_text="Пароль должен содержать минимум 8 символов.",
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Повторите пароль"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]
        labels = {"username": "Имя пользователя"}
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите имя пользователя",
                }
            )
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите имя пользователя"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )
    remember_me = forms.BooleanField(
        required=False,
        label="Запомнить меня",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите адрес электронной почты"}
        )

    def save(
        self,
        domain_override=None,
        subject_template_name="accounts/reset_pwd/password_reset_subject.txt",
        email_template_name="accounts/reset_pwd/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            context = {
                "email": user.email,
                "domain": domain_override or request.get_host(),
                "site_name": "Electro.",
                "uid": uid,
                "user": user,
                "token": token,
                "protocol": "https" if use_https else "http",
            }

            message = render_to_string(
                "accounts/reset_pwd/password_reset_email.html", context
            )

            send_custom_email.delay(
                subject="Восстановление пароля",
                message=message,
                recipient_email=user.email,
            )


class CustomPasswordConfirmFrom(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите новый пароль",
            }
        )
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Повторите новый пароль",
            }
        )
