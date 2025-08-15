from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from Tartas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name='base.html'), name="home"),
    path("accounts/", include("Accounts.urls")),
    path("about", TemplateView.as_view(template_name='about.html'), name="about"),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('addcake/', views.CakeAddView.as_view(), name='add_cake'),
    path("list_cake/", views.CakeListView.as_view(), name="list_cake"),
    path("delete_cake/<int:pk>/", views.DeleteCakeView.as_view(), name="delete_cake"),
    path("update_cake/<int:pk>/", views.UpdateCakeView.as_view(), name="update_cake"),
    path('cart/', include('cart.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
