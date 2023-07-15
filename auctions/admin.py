from django.contrib import admin
from .models import Listing, Category, User, Comments, Bids

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "starting_bid_amount", "current_bid_amount", "owner",  "description", "category", "is_active")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category",)

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("comment","user","listing")

class BidAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "bid_amount")

# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Bids, BidAdmin)
