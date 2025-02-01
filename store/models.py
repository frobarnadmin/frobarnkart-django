from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='photos/products/', blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

#define your category variation here Frobarn
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category = 'color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category = 'size', is_active=True)

#define your category variation here Frobarn
variation_category_choice = (
    ('color', 'Color'),
    ('size', 'Size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=200, choices=variation_category_choice)
    variation_value = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __unicode__(self):
        return self.product
