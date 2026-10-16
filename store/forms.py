from django import forms
from .models import Product


class SellerProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "description",
            "price",
            "material",
            "image",
            "payment_method",
            "payment_number",
            "payment_account_name",
            "deposit_amount",
            "production_time",
            "balance_payment_terms",
        ]
        labels = {
            "name": "Jina la bidhaa",
            "category": "Aina ya samani",
            "description": "Maelezo ya bidhaa",
            "price": "Bei (TSh)",
            "material": "Nyenzo zilizotumika",
            "image": "Picha ya bidhaa",
            "payment_method": "Njia ya malipo",
            "payment_number": "Namba ya malipo",
            "payment_account_name": "Jina la mwenye akaunti",
            "deposit_amount": "Malipo ya awali (TSh)",
            "production_time": "Muda wa kutengeneza",
            "balance_payment_terms": "Masharti ya malipo yaliyobaki",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "balance_payment_terms": forms.TextInput(),
        }
