from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase, Client
import pytest
from django.urls import reverse
from cart.views import *
from Tartas.models import Tartas
from cart.models import Cart, Order, OrderItem


# Create your tests here.
@pytest.mark.django_db
class TestCartModel:
    def test_cart_str_and_price(self):
        user = User.objects.create(username="Ana")
        tarta = Tartas.objects.create(name="Tarta de Chocolate", description="Choco", price=Decimal("12.50"))
        cart = Cart.objects.create(user=user, tarta=tarta, quantity=2)

        assert str(cart) == "Tarta de Chocolate"

        assert cart.price() == Decimal("25.00")


@pytest.mark.django_db
class TestOrderItemModel:
    def test_orderitem_str_and_subtotal(self):
        user = User.objects.create(username="John")
        order = Order.objects.create(user=user)
        tarta = Tartas.objects.create(name="Tarta de Vainilla", description="Yummy", price=Decimal("8.00"))
        item = OrderItem.objects.create(order=order, tarta=tarta, price=Decimal("8.00"), quantity=3)

        assert str(item) == "3 of Tarta de Vainilla"

        assert item.subtotal() == Decimal("24.00")
        assert item.total() == Decimal("24.00")


@pytest.mark.django_db
class TestOrderModel:
    def test_order_str_and_total(self):
        user = User.objects.create(username="Javier")
        order = Order.objects.create(user=user)

        assert str(order) == "Javier"

        tarta1 = Tartas.objects.create(name="Strawberry Cake", description="Fresh", price=Decimal("10.00"))
        tarta2 = Tartas.objects.create(name="Tarta de queso", description="Mniam", price=Decimal("15.00"))

        OrderItem.objects.create(order=order, tarta=tarta1, price=Decimal("10.00"), quantity=2)  # 20
        OrderItem.objects.create(order=order, tarta=tarta2, price=Decimal("15.00"), quantity=1)  # 15

        assert order.total() == Decimal("35.00")



@pytest.mark.django_db
class TestOrderHistoryView:
    def setup_method(self):
        self.client = Client()
        self.url = reverse("cart_history")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        # ponieważ widok jest @login_required, powinien przekierować na login
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_empty_order_history_for_new_user(self):
        user = User.objects.create_user(username="ala", password="pass")
        self.client.login(username="ala", password="pass")

        response = self.client.get(self.url)
        assert response.status_code == 200
        assert list(response.context["orders"]) == []
        assert list(response.context["order_items"]) == []

    def test_order_history_with_data(self):
        user = User.objects.create_user(username="jorge", password="pass")
        self.client.login(username="jorge", password="pass")

        cake = Tartas.objects.create(name="Tarta de queso", description="queso", price=Decimal("15.00"))
        order = Order.objects.create(user=user, is_paid=True)
        item = OrderItem.objects.create(order=order, tarta=cake, quantity=2, price=cake.price)

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert order in response.context["orders"]
        assert item in response.context["order_items"]


@pytest.mark.django_db
class TestPlaceOrderView:
    def setup_method(self):
        self.client = Client()
        self.url = reverse("place_order")

    def test_place_order_creates_order_and_items_and_clears_cart(self):
        user = User.objects.create_user(username="carolina", password="pass")
        self.client.login(username="carolina", password="pass")

        cake1 = Tartas.objects.create(name="Brownie", description="desc", price=Decimal("5.00"))
        cake2 = Tartas.objects.create(name="Tarta de Zanahoria", description="desc", price=Decimal("7.50"))

        Cart.objects.create(user=user, tarta=cake1, quantity=2)
        Cart.objects.create(user=user, tarta=cake2, quantity=1)

        response = self.client.get(self.url)  # widok nie rozróżnia GET/POST
        assert response.status_code == 302
        assert response.url == reverse("view_cart")

        # sprawdzamy, że powstało zamówienie
        order = Order.objects.get(user=user)
        items = OrderItem.objects.filter(order=order)
        assert items.count() == 2

        # sprawdzamy poprawność danych
        brownie_item = items.get(tarta=cake1)
        assert brownie_item.quantity == 2
        assert brownie_item.price == cake1.price

        carrot_item = items.get(tarta=cake2)
        assert carrot_item.quantity == 1
        assert carrot_item.price == cake2.price

        # koszyk powinien być pusty
        assert Cart.objects.filter(user=user).count() == 0