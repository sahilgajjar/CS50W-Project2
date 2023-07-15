from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.category}"

# add category, image url, and description
class Listing(models.Model):

    listing = models.CharField(max_length=64)
    starting_bid_amount = models.IntegerField()
    current_bid_amount = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    description = models.CharField(max_length=1024)
    url = models.CharField(max_length=256)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist_user")
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_listing",blank=True)
    
    def isActive(self):
        return self.is_active

    def __str__(self):
        return f"owner : {self.owner}, item : {self.listing}, starting bid : {self.starting_bid_amount}"

class Bids(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_item")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    bid_amount = models.IntegerField()

    def __str__(self):
        return f"item : {self.listing.owner}, amount : {self.bid_amount}"

class Comments(models.Model):
    comment = models.CharField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_item")

    def __str__(self):
        return f"{self.user} : {self.comment}"
    


