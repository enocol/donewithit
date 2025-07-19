from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """
    Form for creating and updating products.
    """
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'main_image', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
        }