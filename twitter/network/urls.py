from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # API Routes
    path("user", views.user, name="users"),
    path("post/create", views.create, name="create"),  # Create a new post
    path("post", views.post, name="post"),  # Literally all users post
    path("posts/<str:type_p>/<int:page_id>", views.posts, name="posts"),  # All posts from users current user following (only if signed in)
    path("posts/<str:type_p>", views.posts_wo_pg, name="posts_wo_pg"),
    path("posts", views.posts_all, name="posts_all"),
    path("profile/<int:user_id>/<int:page_id>", views.profile, name="profile"),  # All posts from users current user following (only if signed in)
    path("profile/<int:user_id>", views.profile_wo_pg, name="profile_wo_pg"),  # All posts from users current user following (only if signed in)
    path("profile", views.profile_own, name="profile_own"),  # All posts from users current user following (only if signed in)
    path("followers", views.followers, name="followers"),  # All users following current user (only if signed in)
    path("404", views.not_found, name="404"),  # All users following current user (only if signed in)
]


