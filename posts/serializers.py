from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    likes = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "user", "title", "text", "created_at", "likes")
