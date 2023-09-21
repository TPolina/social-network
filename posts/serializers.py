from rest_framework import serializers

from posts.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    likes = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "user", "title", "text", "created_at", "likes")


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Like
        fields = ("id", "user", "post", "created_at")
