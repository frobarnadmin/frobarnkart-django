from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery, Brand
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
    list_display = ('brand_name','is_active',)
    prepopulated_fields = {'slug': ('brand_name',)}
    list_editable = ('is_active',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
admin.site.register(Brand, BrandAdmin)
