from decimal import Decimal

from django.contrib.auth.models import User, Permission
from django.test import TestCase
import pytest
from django.test import Client
from django.urls import reverse
from Tartas.models import Tartas, Category

@pytest.mark.django_db
class TestCategoryModel:
    def test_category_str_returns_display_name(self):
        cat = Category.objects.create(name=1)
        assert str(cat) == cat.get_name_display()


@pytest.mark.django_db
class TestTartasModel:
    def test_tartas_str_returns_name(self):
        tarta = Tartas.objects.create(
            name="Tarta de Chocolate",
            description="Yummy",
            price=Decimal("12.50")
        )
        assert str(tarta) == "Tarta de Chocolate"

    def test_get_products_by_id(self):
        t1 = Tartas.objects.create(name="Cake1", description="desc1", price=10)
        t2 = Tartas.objects.create(name="Cake2", description="desc2", price=20)
        result = Tartas.get_products_by_id([t1.id])
        assert list(result) == [t1]

    def test_get_all_products(self):
        Tartas.objects.create(name="Cake1", description="desc1", price=10)
        Tartas.objects.create(name="Cake2", description="desc2", price=20)
        products = Tartas.get_all_products()
        assert products.count() == 2


@pytest.mark.django_db
class TestCakeAddView:
    def setup_method(self):
        self.client = Client()
        self.url = reverse("add_cake")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        # LoginRequiredMixin → redirect na login
        assert response.status_code == 302
        assert "/login/" in response.url

    def test_forbidden_if_no_permission(self):
        user = User.objects.create_user(username="alice", password="password")
        self.client.login(username="alice", password="password")
        response = self.client.get(self.url)
        # Brak uprawnienia → 403
        assert response.status_code == 403

    def test_get_view_with_permission(self):
        user = User.objects.create_user(username="bob", password="password")
        perm = Permission.objects.get(codename="add_tartas")  # nazwa z permission_required
        user.user_permissions.add(perm)
        self.client.login(username="bob", password="password")

        response = self.client.get(self.url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_post_creates_tarta_and_redirects(self):
        user = User.objects.create_user(username="carol", password="password")
        perm = Permission.objects.get(codename="add_tartas")
        user.user_permissions.add(perm)
        self.client.login(username="carol", password="password")

        data = {
            "name": "New Cake",
            "description": "Test cake",
            "price": "10.50",
        }
        response = self.client.post(self.url, data)

        # powinno przekierować po zapisaniu
        assert response.status_code == 302
        assert response.url == self.url

        # i obiekt powinien istnieć w DB
        assert Tartas.objects.filter(name="New Cake").exists()