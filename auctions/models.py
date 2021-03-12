from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField


class User(AbstractUser):
    pass

class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
    category = models.CharField(max_length=120)

class Listing(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=500)
    price = models.FloatField()
    picture = models.ImageField()
    category = ManyToManyField(Category, related_name="listings")
    date_added = models.DateField(auto_now_add=True)
    date_end = models.DateField()
    user_id = ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

class Bids(models.Model):
    class Meta:
        verbose_name_plural = "bids"
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    item = ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField()

class Comments(models.Model):
    class Meta:
        verbose_name_plural = "comments"
    user = ForeignKey(User, on_delete=models.PROTECT, related_name="comments")
    item = ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=750)

class Watchlist(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="watching")
    item = ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched")
    

