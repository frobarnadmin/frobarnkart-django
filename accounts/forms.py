from django import forms
from .models import Account, UserProfile, Tailor


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs= {
        'placeholder':'Enter Password',
        'class':'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs= {'placeholder':'Confirm Password'}))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number' , 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid': ("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

# class TailorForm(forms.ModelForm):
#     class Meta:
#         model = Tailor
#         exclude = ['account', 'created_at', 'updated_at']
#         widgets = {
#             'business_address': forms.Textarea(attrs={'rows': 3}),
#         }
#
# # forms.py
# from django import forms
# from .models import Tailor

COMMON_INPUT_CLS = "form-control"   # keep or rename to match your CSS
TEXTAREA_CLS = "form-control"

class TailorForm(forms.ModelForm):
    class Meta:
        model = Tailor
        exclude = ["account", "created_at", "updated_at"]
        widgets = {
            "business_name": forms.TextInput(attrs={"class": COMMON_INPUT_CLS, "placeholder": "Business Name"}),
            "brand_name": forms.TextInput(attrs={"class": COMMON_INPUT_CLS, "placeholder": "Brand Name"}),
            "business_address": forms.Textarea(attrs={"class": TEXTAREA_CLS, "rows": 3, "placeholder": "Street, Suite…"}),
            "business_city": forms.TextInput(attrs={"class": COMMON_INPUT_CLS, "placeholder": "City"}),
            "business_state": forms.TextInput(attrs={"class": COMMON_INPUT_CLS, "placeholder": "State/Region"}),
            "business_email_address": forms.EmailInput(attrs={"class": COMMON_INPUT_CLS, "placeholder": "Business Email"}),
            "business_phone_number": forms.TextInput(attrs={"class": COMMON_INPUT_CLS, "placeholder": "+1 (___) ___-____"}),
            "maximum_capacity_per_week": forms.NumberInput(attrs={"class": COMMON_INPUT_CLS, "placeholder": "e.g., 25"}),
            "local_bank": forms.TextInput(attrs={"class": COMMON_INPUT_CLS, "placeholder": "Bank Name"}),
            "bank_account_name": forms.TextInput(attrs={"class": COMMON_INPUT_CLS, "placeholder": "Account Name"}),
            "bank_account_number": forms.TextInput(attrs={"class": COMMON_INPUT_CLS, "placeholder": "Account Number"}),
        }

    # optional: pretty labels
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        labels = {
            "business_name": "Business name",
            "brand_name": "Brand name",
            "business_address": "Business address",
            "business_city": "Business city",
            "business_state": "Business state",
            "business_email_address": "Business email address",
            "business_phone_number": "Business phone number",
            "maximum_capacity_per_week": "Maximum capacity per week",
            "local_bank": "Local bank",
            "bank_account_name": "Bank account name",
            "bank_account_number": "Bank account number",
        }
        for f, lbl in labels.items():
            self.fields[f].label = lbl
