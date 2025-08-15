from django.db import models
from Tartas.models import Tartas


# Create your models here.

class Cart(models.Model):
    tarta = models.ForeignKey(Tartas, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.tarta.name
    def price(self):
        return self.quantity * self.tarta.price

class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def total(self):
        return sum(item.subtotal() for item in self.orderitem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tarta = models.ForeignKey(Tartas, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.tarta.name}"
    def subtotal(self):
        return self.price * self.quantity
    def total(self):
        return self.quantity * self.price