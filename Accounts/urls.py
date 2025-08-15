from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from Accounts import views



urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile')
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)