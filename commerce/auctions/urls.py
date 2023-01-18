from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("add_bid/<int:listing_id>", views.add_bid, name="add_bid"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
]
