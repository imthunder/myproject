from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
# from .tasks import order_created
from django.http import JsonResponse
import json
import urllib.request
# from ..shop.models import Product
from decimal import Decimal

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})

def order_notify(request):
    order = request.POST.get('order')
    order = json.loads(order)
    orderText = "手机号: {0}\n微信号: {1}\n地址: {2}\n时间: {3}".format(order['0'],order['1'],order['2'],order['3'])
    cart = Cart(request)
    cartText = ""

    for product in cart:
        cartText += "{}: {} * {} : {}\n".format(product['product'],product['price'],product['quantity'],Decimal(product['price']) * product['quantity'])

    cartText += '\n总价: {}\n\n'.format(cart.get_total_price())
    dd(cartText + orderText)
    return  JsonResponse({'success':True, 'data':{
                'status_code' : 200,
                'order':order
            }})

def dd(orderText):
    url='https://oapi.dingtalk.com/robot/send?access_token=164879c145dd047d0aa38b56949825fdd36d39b71485ad87483735be0d7c439c'

    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": orderText
        },
    }

    sendData = json.dumps(data)
    sendData = sendData.encode("utf-8")

    request = urllib.request.Request(url=url, data=sendData, headers=header)


    opener = urllib.request.urlopen(request)
    print(opener.read())
