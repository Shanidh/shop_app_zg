from django.urls import path

from customerapp.apis import CustomerLogOutAPI, CustomerLoginAPI, CustomerRegisterAPI
from . import views


urlpatterns = [
    path("customer/register/", views.customer_register, name="customer-register"),
    path("", views.customer_login, name="customer-login"),
    path('customer/products', views.product_list, name='customer_product_list'),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("view_cart/", views.view_cart, name="view_cart"),
    path("update_cart/<int:cart_id>/", views.update_cart, name="update_cart"),
    path("remove_from_cart/<int:cart_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("place_order/", views.place_order, name="place_order"),
     path("add_address/", views.add_address, name="add_address"),
     path("order_summary/<int:order_id>/", views.order_summary, name="order_summary"),
     path("order_status/", views.order_status, name="order_status"),
     path("rate_product/<int:product_id>/", views.rate_product, name="rate_product"),


    path("login/api", CustomerLoginAPI.as_view(), name="customer_login_Api"), 
    path("logout/api", CustomerLogOutAPI.as_view(), name="customer_logout_api"),
    path("register/api", CustomerRegisterAPI.as_view(), name="customer_register_api"),
]