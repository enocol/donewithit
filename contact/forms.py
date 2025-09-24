from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    hp = forms.CharField(required=False, widget=forms.HiddenInput) 

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user
        if user and user.is_authenticated:
            display_name = (getattr(user, "get_full_name", lambda: "")() or user.username)
            self.fields["name"].initial = display_name
            self.fields["email"].initial = user.email
            self.fields["name"].widget.attrs["readonly"] = True
            self.fields["email"].widget.attrs["readonly"] = True
            
            self.fields["name"].required = True
            self.fields["email"].required = True

    def clean_hp(self):
        if self.cleaned_data.get("hp"):
            raise forms.ValidationError("Bot detected.")
        return ""

    def save(self, commit=True):
        message = super().save(commit=False)
        if self._user and self._user.is_authenticated:
            
            message.user = self._user
            message.name = (getattr(self._user, "get_full_name", lambda: "")() or self._user.username)
            message.email = self._user.email
        if commit:
            message.save()
        return message
