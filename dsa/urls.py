from django.urls import path
from .views import RegisterView, login_view, logout_view, email_verification

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('verify/<uuid:code>/', email_verification, name='email_verification'),
]




from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name='cart'),
    path('auth/', views.auth_view, name='auth'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]