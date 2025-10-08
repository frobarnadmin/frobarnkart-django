from django import forms
from .models import Contact, NewsletterContact

class ContactForm(forms.ModelForm):
    # Honeypot (leave empty in the template; bots fill it)
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "phone", "email", "message"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "John"}),
            "last_name":  forms.TextInput(attrs={"placeholder": "Doe"}),
            "phone":      forms.TextInput(attrs={"placeholder": "+1 *** *** ****"}),
            "email":      forms.EmailInput(attrs={"placeholder": "example@gmail.com"}),
            "message":    forms.Textarea(attrs={"placeholder": "Write your enquiry..."}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):  # if honeypot filled -> likely bot
            raise forms.ValidationError("Invalid submission.")
        return cleaned

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterContact
        fields = ["email"]

    def clean_email(self):
        # Normalize emails to lowercase
        return self.cleaned_data["email"].strip().lower()