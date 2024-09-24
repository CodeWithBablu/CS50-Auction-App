from typing import Optional
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('ELE', 'Electronics'),
        ('FAS', 'Fashion'),
        ('HOM', 'Home'),
        ('TOY', 'Toys'),
        ('ART', 'Art'),
        ('INS', 'Musical Instruments'),
    ]
        
    class Meta:
        verbose_name_plural = 'Active Listings'

    title = models.CharField(max_length=64)
    shortdesc = models.CharField(max_length=120)
    desc = models.TextField(max_length=400)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    active = models.BooleanField(default=True)
    image = models.URLField(max_length=500, default='')
    listedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_listings")
    listed_At = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

class WatchList(models.Model):
    class Meta:
        verbose_name_plural = 'Watch List'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlisted_by")

    def __str__(self):
        return f"{self.user.username} is watching {self.listing.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    bidplaced_At = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} bid {self.amount} on {self.listing.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=200)
    commented_At = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.listing.title}: {self.content[:50]}"
