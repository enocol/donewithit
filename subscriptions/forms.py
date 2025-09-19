# newsletter/forms.py
from django import forms
from .models import Subscriber

class NewsletterSignupForm(forms.ModelForm):
    # simple honeypot (bots will fill it; humans won’t see it)
    hp = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Subscriber
        fields = ["email"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["email"].widget.attrs.update({
                "class": "form-control",
                "placeholder": "Enter your email",
                "required": True,
                "label": "Email",
                "type": "email",
            })

    def clean_hp(self):
        if self.cleaned_data.get("hp"):
            raise forms.ValidationError("Bot detected.")
        return ""
