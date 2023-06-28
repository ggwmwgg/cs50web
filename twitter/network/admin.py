from django.contrib import admin
from .models import User, Post, Comment


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "username", "email", "is_staff", "is_superuser", )

    fieldsets = (
        (None, {
            "fields": ("username", "password")
        }),
        ("Personal info", {
            "fields": ("name", "bio", "email", "url",)
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser")
        }),
    )
    list_editable = ("is_staff", "is_superuser", "email",)


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "body", "timestamp",)
    list_filter = ("user",)
    ordering = ('-timestamp',)
    search_fields = ('user',)
    fieldsets = (
        ("Post Info", {
            "fields": ("user", "body",)
        }),
        ("Likes/Comments", {
            "fields": ("likes", "comments",)
        }),
    )


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = (PostInline, )


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "body", "timestamp",)
    list_filter = ("user", "post",)
    ordering = ('-timestamp',)
    search_fields = ('user',)
    fieldsets = (
        ("Comment Info", {
            "fields": ("user", "post", "body", )
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
