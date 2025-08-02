from django.shortcuts import render

from store.models import Product, ReviewRating, Brand


def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    brands = Brand.objects.all().filter(is_active=True).order_by('created_at')

    reviews = ''

    # get the reviews
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
        'brands': brands,
    }
    return render(request, 'home.html', context)

def about(request):

    return render(request, 'about.html')

def faqs(request):

    return render(request, 'faqs.html')

def support(request):

    return render(request, 'support.html')

def contact(request):

    return render(request, 'contact.html')