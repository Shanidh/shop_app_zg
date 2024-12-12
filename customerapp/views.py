from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages

from shop.models import CustomUser, Product, UserType
from customerapp.models import Cart

# Create your views here.
def customer_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, "customer/customer_register.html")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "customer/customer_register.html")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, "customer/customer_register.html")

        # Create the customer user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            user_type=UserType.CUSTOMER,
        )
        user.slug = slugify(username)
        user.save()

        messages.success(request, "customer registered successfully. Please log in.")
        return redirect("customer-login")

    return render(request, "customer/customer_register.html")


def customer_login(request):
    if request.method == "POST":
        # Get username and password from POST request
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validate if both fields are provided
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, "customer/customer_login.html")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        print(user, "user")

        # Check if user exists and is of type customer
        if user is not None and user.user_type == UserType.CUSTOMER:
            login(request, user)  # Log in the user
            return redirect("customer_product_list")  # Redirect to customers list or desired URL
        else:
            # Add an appropriate error message
            if user is None:
                messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "You are not authorized as a customer user.")
    
    # Render the login page
    return render(request, "customer/customer_login.html")


def product_list(request):
    products = Product.objects.all()
    return render(request, "customer/customer_product_list.html", {"products": products})


def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get("quantity", 1))

        # Check if the product is already in the cart
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        messages.success(request, f"{product.name} added to cart successfully!")
        return redirect("customer_product_list")

    return redirect("customer_product_list")


def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_cost = sum(item.total_price() for item in cart_items)
    return render(request, "customer/view_cart.html", {"cart_items": cart_items, "total_cost": total_cost})


def update_cart(request, cart_id):
    if request.method == "POST":
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        quantity = int(request.POST.get("quantity", 1))

        if quantity <= 0:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully!")

    return redirect("view_cart")


def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("view_cart")
