from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from cart import views

urlpatterns = [
    path('main/', views.product_list, name='product_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart_history/', views.order_history, name='cart_history'),
    path('place_order/', views.place_order, name='place_order'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)