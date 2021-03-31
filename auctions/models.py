from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import BooleanField
from django.db.models.fields.related import ForeignKey, ManyToManyField

class User(AbstractUser):
    pass

class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
    category = models.CharField(max_length=120)
    def __str__(self):
        return self.category

class Listing(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    original_price = models.DecimalField(max_digits=12, decimal_places=2, default=price)
    picture = models.ImageField(upload_to='images/', blank=True)
    category = ManyToManyField(Category, related_name="categories")
    date_added = models.DateField(auto_now_add=True)
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    closed = BooleanField(default=False)
    
class Bids(models.Model):
    class Meta:
        verbose_name_plural = "bids"
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    item = ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=12, decimal_places=2)

class Comments(models.Model):
    class Meta:
        verbose_name_plural = "comments"
    user = ForeignKey(User, on_delete=models.PROTECT, related_name="comments")
    item = ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=750)
    date_added = models.DateField(auto_now_add=True)

class Watchlist(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="watching")
    item = ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched")
    

