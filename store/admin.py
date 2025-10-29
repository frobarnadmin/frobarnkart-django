from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery, Brand
from django.utils.html import format_html
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'brand', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active','variation_value',)
    list_filter = ('product', 'variation_category', 'variation_value',)

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'status')
    list_editable = ('status',)
    list_filter = ('product', 'rating')

class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ('product',)

class BrandAdmin(admin.ModelAdmin):
    # list_display = ('brand_name','is_active',)
    prepopulated_fields = {'slug': ('brand_name',)}
    list_editable = ('is_active',)
    list_display = ("brand_name", "brand_company_name", "is_active", "created_at", "logo_thumb")
    list_filter = ("is_active","brand_company_name", )
    search_fields = ("brand_name", "brand_company_name__business_name")
    readonly_fields = ("logo_preview", "created_at", "updated_at")
    fields = (
        "brand_name",
        "slug",
        "brand_image_logo",
        "logo_preview",          # <— shows the image
        "brand_description",
        "brand_company_name",
        "is_active",
        "created_at",
        "updated_at",
    )

    def logo_preview(self, obj):
        """Large preview on the change page."""
        if obj and obj.brand_image_logo:
            return format_html(
                '<img src="{}" style="max-height:180px;border-radius:8px"/>',
                obj.brand_image_logo.url,
            )
        return "No logo uploaded"

    logo_preview.short_description = "Current logo"

    def logo_thumb(self, obj):
        """Small thumbnail in list view."""
        if obj.brand_image_logo:
            return format_html('<img src="{}" style="height:40px"/>', obj.brand_image_logo.url)
        return "—"

    logo_thumb.short_description = "Logo"


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
admin.site.register(Brand, BrandAdmin)
