from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import CustomUser, UserType, Product
from django.utils.text import slugify
from django.contrib import messages


def shop_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, "shop/shop_register.html")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "shop/shop_register.html")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, "shop/shop_register.html")

        # Create the Shop user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            user_type=UserType.SHOP,
        )
        user.slug = slugify(username)
        user.save()

        messages.success(request, "Shop registered successfully. Please log in.")
        return redirect("shop-login")

    return render(request, "shop/shop_register.html")


def shop_login(request):
    if request.method == "POST":
        # Get username and password from POST request
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validate if both fields are provided
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, "shop/shop_login.html")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # Check if user exists and is of type SHOP
        if user is not None and user.user_type == UserType.SHOP:
            login(request, user)  # Log in the user
            return redirect("customer-list")  # Redirect to customers list or desired URL
        else:
            # Add an appropriate error message
            if user is None:
                messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "You are not authorized as a Shop user.")
    
    # Render the login page
    return render(request, "shop/shop_login.html")


@login_required
def customer_list(request):
    """View to list all customers."""
    if request.user.user_type == "SHOP":
        customers = CustomUser.objects.filter(user_type="CUSTOMER")
        return render(request, "shop/customer_list.html", {"customers": customers})
    else:
        return render(request, "shop/unauthorized.html")
    

def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")

        if not name or not price:
            messages.error(request, "Name and Price are required.")
            return render(request, "shop/add_product.html")

        try:
            price = float(price)
        except ValueError:
            messages.error(request, "Invalid price value.")
            return render(request, "shop/add_product.html")

        Product.objects.create(name=name, description=description, price=price)
        messages.success(request, "Product added successfully!")
        return redirect("product_list")

    return render(request, "shop/add_product.html")    


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")

        if not name or not price:
            messages.error(request, "Name and Price are required.")
            return render(request, "shop/edit_product.html", {"product": product})

        try:
            price = float(price)
        except ValueError:
            messages.error(request, "Invalid price value.")
            return render(request, "shop/edit_product.html", {"product": product})

        product.name = name
        product.description = description
        product.price = price
        product.save()

        messages.success(request, "Product updated successfully!")
        return redirect("product_list")

    return render(request, "shop/edit_product.html", {"product": product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("product_list")

    return render(request, "shop/delete_product.html", {"product": product})


def product_list(request):
    products = Product.objects.all()
    return render(request, "shop/product_list.html", {"products": products})
