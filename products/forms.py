from django import forms
from .models import Category, Product
from .models import MoreProductImage
from cloudinary.forms import CloudinaryFileField

class ProductForm(forms.ModelForm):
    """
    Form for creating and updating products.
    """
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'main_image', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'placeholder': 'Enter product name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Enter product description'})
        self.fields['price'].widget.attrs.update({'placeholder': 'Enter product price'})
        self.fields['category'].choices = [(cat.id, cat.get_display_name()) for cat in Category.objects.all()]
        self.fields['category'].required = True
        self.fields['category'].label = "Product Category"
        self.fields['category'].empty_label = "Select a category"  # Optional: Set an empty label for the category field
        self.fields['main_image'].required = True
        self.fields['main_image'].help_text = "Upload the main image for the product"
        self.fields['main_image'].widget.attrs.update({'accept': 'image/*'})
        self.fields['main_image'].label = "Main Image"
        

class MoreProductImageForm(forms.ModelForm):
    # image = CloudinaryFileField()  # optional if you want widget integration

    class Meta:
        model = MoreProductImage
        fields = ['image']


MoreProductImageFormSet = forms.inlineformset_factory(
    Product,
    MoreProductImage,
    form=MoreProductImageForm,
    fields=['image'],
    max_num=5,  # Maximum number of images allowed
    min_num=0,  # Minimum number of images required
    validate_min=True,
    validate_max=True,
    labels={
        'image': 'Additional Image (optional)'
    },
    extra=3,  # Number of image forms to show by default
    can_delete= False
)