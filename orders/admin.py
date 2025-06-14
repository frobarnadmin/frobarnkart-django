from django.contrib import admin
from orders.models import Order, Payment, OrderProduct, UserMeasurement


# Register your models here.
class OrderedProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('ordered','payment','user', 'product', 'quantity', 'product_price')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'ip', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email' ]
    readonly_fields = ('payment','order_number', 'is_ordered')
    list_per_page = 20
    inlines = [OrderedProductInline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'payment', 'user', 'created_at']

class UserMeasurementAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'user',
        'neck',
        'chest',
        'waist',
        'hips',
        'inseam_to_ankle',
        'created_at'
    )
    search_fields = ('user__username', 'user__email')  # Adjust based on Account model fields
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(UserMeasurement, UserMeasurementAdmin)