from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('brand/<slug:brand_slug>/', views.brand_detail, name='brand_detail'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]
