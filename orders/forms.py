from django import forms
from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "email", "phone", "address"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите ваше ФИО"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Введите ваш Email"}
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите ваш номер телефона",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите адрес доставки",
                    "rows": 3,
                }
            ),
        }
        labels = {
            "full_name": "ФИО",
            "email": "Email",
            "phone": "Номер телефона",
            "address": "Адрес доставки",
        }
