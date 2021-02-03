from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=64)
    body = models.CharField(max_length=360)
    isOpen = models.BooleanField()
    price = models.IntegerField()
    imageURL = models.CharField(max_length=360)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    price = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.creator} bid {self.listing}, for {self.price}"

class Comment(models.Model):
    body = models.CharField(max_length=280)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.creator} posted on {self.listing}: '{self.body}'"

class Category(models.Model):
    name = models.CharField(max_length=64)
    listings = models.ManyToManyField(Listing, blank=True, related_name="category")

    def __str__(self):
        return f"{self.name}"

class Watchlists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listings = models.ManyToManyField(Listing, blank=True, related_name="watchlists")