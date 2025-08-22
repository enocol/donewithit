from django import forms
from django.forms import inlineformset_factory
from products.models import Product, MoreProductImage, Category

class ProductEditForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label="Product Category",
        empty_label="Select a category",
    )

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'main_image', 'category']
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter product description'}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'placeholder': 'Enter product price'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Don’t force a re-upload when editing
        self.fields['main_image'].required = False
        self.fields['main_image'].label = "Main Image"
        self.fields['main_image'].help_text = "Upload to replace the current main image (optional)."
        self.fields['main_image'].widget.attrs.update({'accept': 'image/*'})

class MoreProductImageForm(forms.ModelForm):
    class Meta:
        model = MoreProductImage
        fields = ['image']
        

MoreProductImageFormSet = inlineformset_factory(
    Product,
    MoreProductImage,
    form=MoreProductImageForm,
    fields=['image'],
    extra=1,          # show 1 empty row by default
    max_num=5,        # total cap
    validate_max=True,
    can_delete=True,  # allow removing existing images
)
