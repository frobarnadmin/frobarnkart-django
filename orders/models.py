from django.db import models

from accounts.models import Account
from store.models import Variation, Product
# from django.contrib.auth.models import User
# from django.contrib.postgres.fields import JSONField  # Use from django.db.models if Django >= 3.1
from django.db.models import JSONField

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.FloatField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    #add zipcode here
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return "%s %s" % (self.first_name.capitalize(), self.last_name.capitalize())

    def full_address(self):
        return "%s %s" % (self.address_line_1, self.address_line_2)

    def __str__(self):
        return self.first_name + " " + self.last_name + " #" + self.order_number

#ordered products model
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name + " #" + self.order.order_number

# remove blank and null = true for order at a later time
class UserMeasurement(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='measurements')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    neck = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    chest = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    stomach = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    trousers_waist = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hips = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    thigh_right = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    thigh_left = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    knee_right = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    knee_left = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    armhole_right = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    armhole_left = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    bicep_left = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    bicep_right = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    wrist_right = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    wrist_left = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    crotch = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    arm_length_to_wrist = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    outside_leg_to_ground = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    inseam_to_ground = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    inseam_to_ankle = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    straight_shoulder = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    curve_shoulder = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    neck_to_chest = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    neck_to_waist_front = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    neck_to_waist_back = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    neck_to_crotch_backlong = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    neck_to_middle_hand_frontlong = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    neck_to_knee = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    neck_high_to_knee = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Measurements"


class UserMeasurementData(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, default="1970010101")
    data = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Measurements_"


class TailorComment(models.Model):
    order_product = models.ForeignKey('OrderProduct', on_delete=models.CASCADE, related_name='tailor_comments')
    comment_title = models.CharField(max_length=255, blank=True)  # Optional title
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment_title if self.comment_title else f"Comment #{self.pk}"