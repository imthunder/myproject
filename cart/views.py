from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from django.http import JsonResponse

@require_POST
def cart_add(request):
    cart = Cart(request)
    # , product_id, count
    product_id = request.POST.get('product_id')
    count = int(request.POST.get('count'))
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product,
             quantity=count,
             update_quantity=True)
    return  JsonResponse({'success':True, 'data':{
                'status_code' : 200,
                'cart':cart.cart
            }})

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                            initial={'quantity': item['quantity'],
                            'update': True})
    coupon_apply_form = CouponApplyForm()

    return render(request,
                  'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form})
