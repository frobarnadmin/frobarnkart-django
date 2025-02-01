from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from carts.models import Cart, CartItem
from store.models import Product, Variation


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    #step 1 get the product to be added to the cart
    product = Product.objects.get(id=product_id)

    product_variation = []

    # handle POST request coming in
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
                # print(variation.variation_value, "  ", variation.variation_category)

            except:
                pass
    print(product_variation)



    #step 2 create a cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product = product, cart = cart).exists()

    #step 3 add to a cart item or create a new cart item
    # if cart item exists, then add one more quantity to existing variation. Or add new variation
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart,)

        ex_var_list = [] #existing variation list for cartitem
        id = [] #cartItem id
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
#watchout from experience. order matters here Frobarn
        # if newly selected product variation is in existing variation, then add +1 quantity
        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product = product, id=item_id)
            item.quantity += 1
            item.save()
        # if newly selected product variation is NOT in existing variation, then add new variation
        else:
            item= CartItem.objects.create(product=product, cart=cart, quantity=1)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    # if cart item does not exist. Then create a new one
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()

    #step 4 take be to cart function
    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request)) #select the active cart
    product = get_object_or_404(Product, id=product_id) #get the product that need to be decremented
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id= cart_item_id)  #select the particular cart item that belongs to the cart
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id= cart_item_id)
    cart_item.delete()
    return redirect('cart')



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request)) # the session_key, hence the _cart_id is persistent on the website
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) #total amount of all product in the cart
            quantity += cart_item.quantity #total quantity in all the cart
        tax = (2 * total) / 100 # 2% tax applied
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)