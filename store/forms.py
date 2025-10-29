from django import forms
from .models import ReviewRating, Brand
from django.utils.text import slugify
from accounts.models import Tailor

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject','review','rating']


class BrandCreateForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["brand_name", "brand_image_logo", "brand_description"]  # ← removed is_active
        widgets = {
            "brand_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Frobarn Couture"}),
            "brand_description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        if not self.request or not self.request.user.is_authenticated:
            raise forms.ValidationError("You must be logged in.")
        if not getattr(self.request.user, "is_tailor", False):
            raise forms.ValidationError("Only tailors can create brands.")
        if not Tailor.objects.filter(account=self.request.user).exists():
            raise forms.ValidationError("Complete your tailor profile before creating a brand.")
        return cleaned

    def _unique_slug(self, base):
        from .models import Brand
        base_slug = slugify(base) or "brand"
        slug = base_slug
        i = 2
        while Brand.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{i}"
            i += 1
        return slug

    def save(self, commit=True):
        brand = super().save(commit=False)
        tailor = Tailor.objects.get(account=self.request.user)
        brand.brand_company_name = tailor

        if not brand.slug:
            brand.slug = self._unique_slug(brand.brand_name)

        # DO NOT expose or change is_active here; leave model default / admin control
        if commit:
            brand.save()
        return brand
#
# class BrandCreateForm(forms.ModelForm):
#     class Meta:
#         model = Brand
#         fields = ["brand_name", "brand_image_logo", "brand_description", "is_active"]
#         widgets = {
#             "brand_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Frobarn Couture"}),
#             "brand_description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
#             "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         # Expect request to be passed in by the view
#         self.request = kwargs.pop("request", None)
#         super().__init__(*args, **kwargs)
#
#     def clean(self):
#         cleaned = super().clean()
#         # Ensure this user is a tailor with a Tailor record
#         if not self.request or not self.request.user.is_authenticated:
#             raise forms.ValidationError("You must be logged in.")
#         if not getattr(self.request.user, "is_tailor", False):
#             raise forms.ValidationError("Only tailors can create brands.")
#         if not Tailor.objects.filter(account=self.request.user).exists():
#             raise forms.ValidationError("Complete your tailor profile before creating a brand.")
#         return cleaned
#
#     def _unique_slug(self, base):
#         """Generate a unique slug from brand_name."""
#         from .models import Brand
#         base_slug = slugify(base) or "brand"
#         slug = base_slug
#         idx = 2
#         while Brand.objects.filter(slug=slug).exists():
#             slug = f"{base_slug}-{idx}"
#             idx += 1
#         return slug
#
#     def save(self, commit=True):
#         brand = super().save(commit=False)
#         tailor = Tailor.objects.get(account=self.request.user)
#         brand.brand_company_name = tailor
#
#         # If your model’s slug is blank by default, set it here safely
#         if not brand.slug:
#             brand.slug = self._unique_slug(brand.brand_name)
#
#         if commit:
#             brand.save()
#         return brand
