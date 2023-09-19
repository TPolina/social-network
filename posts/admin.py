from django.contrib import admin

from posts.models import Post, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created_at"]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["post", "user", "created_at"]
