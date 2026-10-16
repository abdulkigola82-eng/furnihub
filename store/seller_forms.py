from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .seller_models import SellerProfile


class SellerRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        label="Barua pepe",
    )
    business_name = forms.CharField(
        max_length=200,
        label="Jina la biashara",
    )
    phone = forms.CharField(
        max_length=30,
        label="Namba ya simu",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "business_name",
            "phone",
            "password1",
            "password2",
        )
        labels = {
            "username": "Jina la mtumiaji",
        }

    def clean_business_name(self):
        name = self.cleaned_data["business_name"].strip()
        if not name:
            raise forms.ValidationError(
                "Tafadhali weka jina la biashara."
            )
        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not phone:
            raise forms.ValidationError(
                "Tafadhali weka namba ya simu."
            )
        return phone
