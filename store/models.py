from django.db import models

from accounts.models import Account
from category.models import Category
from django.urls import reverse
from django.db.models import Avg, Count
from accounts.models import Tailor

# Create your models here.

class Brand(models.Model):
    brand_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=200, default='', unique=True)
    brand_image_logo = models.ImageField(upload_to='brand_logos/')
    brand_description = models.TextField(blank=True, null=True)
    brand_company_name = models.ForeignKey(
        Tailor,
        on_delete=models.SET_NULL,
        related_name='brands',
        null=True,
    )
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('brand_detail', args=[self.slug])

    def __str__(self):
        return self.brand_name

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=2000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='photos/products/', blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


    def __str__(self):
        return self.product_name

#define your category variation here Frobarn
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category = 'color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category = 'size', is_active=True)

    def cuffs(self):
        return super(VariationManager, self).filter(variation_category = 'cuff', is_active=True)

    def top_length(self):
        return super(VariationManager, self).filter(variation_category = 'top_length', is_active=True)

    def leg_opening(self):
        return super(VariationManager, self).filter(variation_category = 'leg_opening', is_active=True)

    def fabric(self):
        return super(VariationManager, self).filter(variation_category = 'fabric', is_active=True)

    def top_fit(self):
        return super(VariationManager, self).filter(variation_category = 'top_fit', is_active=True)

    def embroidery(self):
        return super(VariationManager, self).filter(variation_category = 'embroidery', is_active=True)

#define your category variation here Frobarn
variation_category_choice = (
    ('color', 'Color'),
    ('size', 'Size'),
    ('cuff', 'Cuff'),
    ('top_length', 'Top Length'),
    ('leg_opening', 'Leg Opening'),
    ('fabric', 'Fabric'),
    ('top_fit', 'Top Fit'),
    ('embroidery', 'Embroidery'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=200, choices=variation_category_choice)
    variation_value = models.CharField(max_length=200)
    image = models.ImageField(upload_to='variation_images/', blank=True)
    video_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):  # Use __str__ in modern Django applications
        return f"{self.product} - {self.variation_category}: {self.variation_value}"

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=False)
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.user}: {self.rating}"

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='gallery/', blank=True)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name_plural = "Product Gallery"
