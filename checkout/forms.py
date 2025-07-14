from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    """
    Form for the checkout process.
    """

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'address',
            'city', 'state', 'post_code', 'country'
        ]

    def clean(self):
        cleaned_data = super().clean()
        # Additional validation can be added here
        return cleaned_data