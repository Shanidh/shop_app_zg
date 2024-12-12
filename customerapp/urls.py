from django.urls import path
from . import views


urlpatterns = [
    path("customer/register/", views.customer_register, name="customer-register"),
    path("", views.customer_login, name="customer-login"),
    path('customer/products', views.product_list, name='customer_product_list'),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("view_cart/", views.view_cart, name="view_cart"),
    path("update_cart/<int:cart_id>/", views.update_cart, name="update_cart"),
    path("remove_from_cart/<int:cart_id>/", views.remove_from_cart, name="remove_from_cart"),
]