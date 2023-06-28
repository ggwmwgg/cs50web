from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment, Watchlist


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff", "is_superuser", "last_login",)
    fieldsets = (
        (None, {
            "fields": ("username", "password")
        }),
        ("Personal info", {
            "fields": ("first_name", "last_name", "email")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important dates", {
            "fields": ("last_login", "date_joined")
        }),
    )
    list_editable = ("is_staff", "is_superuser",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_editable = ("name",)
    ordering = ('id',)
    search_fields = ('name',)
    fieldsets = (
        ("Category Name", {
            "fields": ("name", )
        }),
    )


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "starting_bid", "current_bid", "is_active", "date")
    list_editable = ("title", "user", "starting_bid", "is_active",)
    fieldsets = (
        ("Main Info", {
            "fields": ("title", "description", "date",)
        }),
        ("Bids", {
            "fields": ("starting_bid", "current_bid",)
        }),
        ("Other Info", {
            "fields": ("image_url", "category", "user",)
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
    )
    readonly_fields = ("current_bid", "date",)
    ordering = ('id',)


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bid", "user", "listing", "date")
    list_filter = ("user", "listing")
    ordering = ('listing', '-bid')
    search_fields = ('user',)


class CommentAdmin(admin.ModelAdmin):
    list_display_links = ("id",)
    list_display = ("id", "comment", "user", "listing", "date")
    list_editable = ("comment",)
    list_filter = ("user", "listing")
    ordering = ('id',)


class WatchlistAdmin(admin.ModelAdmin): # TO DO
    list_display = ("user", "listings_string")
    list_filter = ("user", )
    ordering = ('user',)
    search_fields = ('user',)
    filter_horizontal = ("listing",)
    fieldsets = (
        ("User (Don't change this field, instead create a new watchlist for new user)", {
            "fields": ("user",)
        }),
        ("Listings", {
            "fields": ("listing",)
        }),
    )

    def listings_string(self, obj):
        return ", ".join([str(f"{item.id}|{item.title}|{item.user}") for item in obj.listing.all()])
    listings_string.short_description = "Listings"


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.site_header = "Auctions Administration"
admin.site.site_title = "Auctions Admin Portal"
admin.site.index_title = "Welcome to Auctions Portal"
