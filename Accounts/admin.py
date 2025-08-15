from Accounts.models import *

from django.contrib import admin
from Tartas.models import *
from cart.models import *

admin.site.register(Category)
admin.site.register(Tartas)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
