from django.db import models
from django.contrib.auth import get_user_model

# from shop.models import Product
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=255, help_text=_("Product name"))
    description = models.TextField(help_text=_("Product description"))
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        ratings = Rating.objects.filter(product=self)
        if ratings.exists():
            return ratings.aggregate(models.Avg('score'))['score__avg']
        return None

    def __str__(self):
        return self.name  

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="India")

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state}, {self.country}"


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        COMPLETED = "COMPLETED", _("Completed")
        CANCELLED = "CANCELLED", _("Cancelled")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def total_price(self):
        return self.quantity * self.price   


   
    

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # String reference
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # String reference
    score = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # Prevent multiple ratings from the same user

    def __str__(self):
        return f"{self.user.username} rated {self.product.name} - {self.score}"
