from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    # add many-to-many field for watching listings
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watchers")


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Categories"


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.URLField(max_length=256, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_listings", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def bids(self):
        return self.listing_bids.all()

    def __str__(self):
        return f"{self.id} | {self.title} | {self.user}"


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    date = models.DateTimeField(auto_now_add=True)

   
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    date = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listing = models.ManyToManyField(Listing, related_name="listings_watchlist", blank=True)
    def __str__(self):
        return f"{self.id} | {self.listing} | {self.user}"
    #function that returns all listings objects in watchlist for user
    def get_listings(self):
        return self.listing.all()


