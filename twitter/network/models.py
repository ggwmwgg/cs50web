from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # creating user model fields for twitter
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25, unique=True, null=False, default="")
    name = models.CharField(max_length=100, default="")
    bio = models.TextField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    following = models.ManyToManyField("User", blank=True, related_name="followers")
    saved_posts = models.ManyToManyField("Post", blank=True, related_name="saved_posts")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
            "url": self.url,
            "following": [user.name for user in self.following.all()],
            "followers": [user.name for user in self.followers.all()]
        }

    def __str__(self):
        return f"{self.id} | {self.username}"


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    comments = models.ManyToManyField("Comment", blank=True, related_name="comments")

    def serialize(self, user=None):
        is_liked = False
        is_saved = False

        if user:
            is_liked = user in self.likes.all()
            is_saved = self in user.saved_posts.all()

        return {
            "id": self.id,
            "user_id": self.user.id,
            "user": self.user.name,
            "username": self.user.username,
            "image": self.user.url,
            "body": self.body,
            'timestamp': self.timestamp.strftime('%b %d %Y, %I:%M %p'),
            'likes': self.likes.count(),
            'comments': [comment.serialize() for comment in self.comments.all()],
            'comments_count': self.comments.count(),
            'is_liked': is_liked,
            'is_saved': is_saved
        }

    def __str__(self):
        return f"{self.id} | {self.user} | {self.body}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ManyToManyField(User, related_name="user")
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ManyToManyField(Post, related_name="post")
    body = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.id} | {self.body}"

    def serialize(self):
        user = self.user.first()
        user_data = [{"name": user.name, "url": user.url, "username": user.username, "user_id": user.id}]
        return {
            "id": self.id,
            "user": self.user.name,
            "users_data": user_data,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%d.%m.%Y %H:%M")
        }
