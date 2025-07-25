from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from carts.models import CartItem
from store.models import Product
from .forms import OrderForm
# from .models import Order, Payment, OrderProduct

import datetime

from .models import Order, OrderProduct, Payment, UserMeasurementData
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json


MEASUREMENT_KEYS = {
    1: "Neck", 2: "Chest", 3: "Waist", 4: "Stomach", 5: "Trousers waist",
    6: "Hips", 7: "Thigh Right", 8: "Thigh Left", 9: "Knee Right", 10: "Knee Left",
    11: "Armhole Right", 12: "Armhole Left", 13: "Bicep Left", 14: "Bicep Right",
    15: "Wrist Right", 16: "Wrist Left", 17: "Crotch", 18: "Arm Length to Wrist",
    19: "Outside Leg to Ground", 20: "Inseam to Ground", 21: "Inseam to Ankle",
    22: "Straight Shoulder", 23: "Curve Shoulder", 24: "Neck to Chest",
    25: "Neck to Waist", 26: "Neck to Waist", 27: "Neck to Crotch",
    28: "Neck to Middle Hand", 29: "Neck to Knee", 30: "Neck High to Knee"
}

def payments(request):
    #this comes from json javascript from paypal
    body = json.loads(request.body)
    print(body)
    order =Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        amount_paid=order.order_total,
        payment_method=body['payment_method'],
        status=body['status'],
    )
    payment.save()

    #update the order
    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order(ed) Product table
    cart_items = CartItem.objects.filter(user = request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

    # Reduce the quantity of the sold products
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear the cart
    CartItem.objects.filter(user = request.user).delete()

    # Send order received email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.content_subtype = 'html'  # Set email content to HTML
    send_email.send()

    # Send order number and transaction id back to sendData method via Json Method (java script in payments.html)
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)

# Create your views here.
def place_order(request, total = 0, quantity = 0):
    current_user = request.user
    #if cart count is <=0, return user to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
            return redirect('store')

    grand_total = 0
    tax = 0.0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity = cart_item.quantity

    tax = (2 * total)/ 100
    grand_total = tax + total

    if request.method == 'POST':
        #map the Post input to the ModelForm/OrderForm
        form = OrderForm(request.POST)
        if form.is_valid():
            #store all the billing information from the POST input in the order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, order_number=order_number, is_ordered=False)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    request.session['order_number_in_session'] = order_number

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id = order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id = transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context) #get measured
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')



# def order_complete(request):
#     order_number = request.GET.get('order_number')
#     transID = request.GET.get('payment_id')
#
#     try:
#         order = Order.objects.get(order_number=order_number, is_ordered=True)
#         ordered_products = OrderProduct.objects.filter(order_id=order.id)
#
#         subtotal = 0
#         for i in ordered_products:
#             subtotal += i.product_price * i.quantity
#
#         payment = Payment.objects.get(payment_id=transID)
#
#         # Read cookie
#         raw_cookie_data = request.COOKIES.get('abody_scan_data')
#         measurement_data = {}
#
#         if raw_cookie_data:
#             try:
#                 parsed_data = json.loads(raw_cookie_data)
#                 # Map ID -> name
#                 measurement_data = {
#                     MEASUREMENT_KEYS.get(int(k), f"Unknown-{k}"): v
#                     for k, v in parsed_data.items()
#                 }
#
#                 # Associate with user (assuming request.user is authenticated)
#                 user = request.user
#                 if user.is_authenticated:
#                     UserMeasurementData.objects.update_or_create(
#                         user=user,
#                         defaults={'data': measurement_data}
#                     )
#             except (json.JSONDecodeError, ValueError) as e:
#                 print("Invalid cookie format:", e)
#
#         context = {
#             'order': order,
#             'ordered_products': ordered_products,
#             'order_number': order_number,
#             'transID': payment.payment_id,
#             'payment': payment,
#             'subtotal': subtotal
#         }
#         return render(request, 'orders/order_complete.html', context)
#
#     except (Payment.DoesNotExist, Order.DoesNotExist):
#         return redirect('home')




@csrf_exempt
@login_required
def save_user_measurements(request):
    order_number_in_session_value = request.session.get('order_number_in_session', '012345')
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            raw_data = json.loads(payload.get('abody_scan_data', '{}'))

            parsed_data = {
                MEASUREMENT_KEYS.get(int(k), f"Unknown-{k}"): v
                for k, v in raw_data.items()
            }

            UserMeasurementData.objects.create(
                user=request.user,
                order_number=order_number_in_session_value,
                data=parsed_data  # set directly
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=405)