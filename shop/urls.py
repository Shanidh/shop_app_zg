from django.urls import path
from . import views

urlpatterns = [
    path("shop/register/", views.shop_register, name="shop-register"),
    path("shop/login/", views.shop_login, name="shop-login"),
    path('customers/', views.customer_list, name='customer-list'),
    path('products', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path("admin/login/", views.shop_login, name="admin-login"),
]
