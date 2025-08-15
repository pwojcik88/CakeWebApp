from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Tartas.models import Tartas
from cart.models import Order, OrderItem, Cart
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def product_list(request):
    products = Tartas.objects.all()
    return render(request, 'index.html', {'product': products})

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.tarta.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    tarta = Tartas.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(tarta=tarta, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return HttpResponseRedirect(reverse('view_cart'))

def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id, user=request.user)
    cart_item.delete()
    return HttpResponseRedirect(reverse('view_cart'))

@login_required
def order_history(request):
    order_items = OrderItem.objects.filter(order__user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'history.html', {'orders': orders, 'order_items': order_items})

def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    order = Order.objects.create(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(order=order, tarta=item.tarta, quantity=item.quantity, price=item.tarta.price)
    cart_items.delete()
    return HttpResponseRedirect(reverse('view_cart'))