from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path("newsletter/subscribe/", views.subscribe_newsletter, name="newsletter_subscribe"),
    # path('payments/', views.payments, name='payments'),
    # path('order_complete/', views.order_complete, name='order_complete'),#get measured
    # path('save-user-measurements/', views.save_user_measurements, name='save_user_measurements'),
]