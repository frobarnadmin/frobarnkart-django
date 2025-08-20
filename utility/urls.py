from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    # path('payments/', views.payments, name='payments'),
    # path('order_complete/', views.order_complete, name='order_complete'),#get measured
    # path('save-user-measurements/', views.save_user_measurements, name='save_user_measurements'),
]