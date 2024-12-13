from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages

from shop.models import CustomUser, UserType
from customerapp.models import Address, Cart, Order, OrderItem, Product, Rating

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
    delete_order_item_by_id(1)
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
    addresses = Address.objects.filter(user=request.user)
    return render(request, "customer/view_cart.html", {
        "cart_items": cart_items,
        "total_cost": total_cost,
        "addresses": addresses,
    })


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


def place_order(request):
    if request.method == "POST":
        address_id = request.POST.get("address")
        if not address_id:
            messages.error(request, "Please select an address.")
            return redirect("view_cart")

        address = get_object_or_404(Address, id=address_id, user=request.user)

        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items:
            messages.error(request, "Your cart is empty!")
            return redirect("view_cart")

        # Calculate total price
        total_price = sum(item.total_price() for item in cart_items)

        # Create the order
        order = Order.objects.create(user=request.user, address=address, total_price=total_price)

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        # Clear the cart
        cart_items.delete()

        messages.success(request, "Your order has been placed successfully!")
        return redirect("order_summary", order_id=order.id)

    # Redirect back to the cart if accessed via GET
    return redirect("view_cart")


def add_address(request):
    if request.method == "POST":
        address_line1 = request.POST.get("address_line1")
        address_line2 = request.POST.get("address_line2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal_code = request.POST.get("postal_code")
        country = request.POST.get("country", "India")

        Address.objects.create(
            user=request.user,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
        )
        messages.success(request, "Address added successfully!")
        return redirect("place_order")

    return render(request, "customer/add_address.html")


def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "customer/order_summary.html", {"order": order})


def order_status(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "customer/order_status.html", {"orders": orders})


def rate_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        score = int(request.POST.get("score"))

        # Check if the user has already rated this product
        existing_rating = Rating.objects.filter(product=product, user=request.user).first()
        if existing_rating:
            existing_rating.score = score
            existing_rating.save()
            messages.success(request, "Your rating has been updated!")
        else:
            Rating.objects.create(product=product, user=request.user, score=score)
            messages.success(request, "Thank you for your rating!")

        return redirect("customer_product_list")

    return render(request, "customer/rate_product.html", {"product": product})


def delete_order_item_by_id(order_item_id):
    try:
        order_item = OrderItem.objects.get(id=order_item_id)
        order_item.delete()
        return f"Order item with ID {order_item_id} has been deleted."
    except OrderItem.DoesNotExist:
        return f"Order item with ID {order_item_id} does not exist."