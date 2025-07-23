from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


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
        model = User
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
        if User.objects.filter(email=email).exists():
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
