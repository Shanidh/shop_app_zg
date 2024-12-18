from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from django.conf import settings

# from customerapp.models import Rating

# from customerapp.models import Rating
# User = get_user_model()

# Create your models here.


class UserType(models.TextChoices):
    SHOP = "SHOP", _("Shop")
    CUSTOMER = "CUSTOMER", _("Customer")


class CustomUser(AbstractUser):
    """Model definition for User."""

    error_messages = {"slug": {"unique": "Username Already Exists."}}

    first_name = None
    last_name = None
    groups = None
    user_permissions = None
    date_joined = None 

    
    user_type = models.CharField(
        help_text=_("User Type"),
        max_length=20,
        choices=UserType.choices,
        null=True,
    )

    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        """Unicode representation of User."""
        return self.username

    def save(self, *args, **kwargs):
        """Save method for User."""
        self.slug = slugify(self.username)
        return super().save(*args, **kwargs)


# class Product(models.Model):
#     name = models.CharField(max_length=255, help_text=_("Product name"))
#     description = models.TextField(help_text=_("Product description"))
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def average_rating(self):
#         ratings = Rating.objects.filter(product=self)
#         if ratings.exists():
#             return ratings.aggregate(models.Avg('score'))['score__avg']
#         return None

#     def __str__(self):
#         return self.name

# class Rating(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ratings")
#     value = models.PositiveIntegerField()  # Assume ratings are from 1 to 5
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Rating: {self.value} for {self.product.name}"


# class Rating(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
#     score = models.PositiveIntegerField(null=True)  # Assuming a score from 1 to 5
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('product', 'user')  # Prevent multiple ratings from the same user

#     def __str__(self):
#         return f"{self.user.username} rated {self.product.name} - {self.score}"