from django import forms

class CheckoutForm(forms.Form):
    """
    Form for the checkout process.
    """
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    email = forms.EmailField(required=True, label='Email Address')
    address = forms.CharField(widget=forms.Textarea, required=True, label='Shipping Address')
    city = forms.CharField(max_length=100, required=True, label='City')
    state = forms.CharField(max_length=100, required=True, label='State/Province')
    post_code = forms.CharField(max_length=20, required=True, label='Post Code')
    country = forms.CharField(max_length=100, required=True, label='Country')

    def clean(self):
        cleaned_data = super().clean()
        # Additional validation can be added here
        return cleaned_data