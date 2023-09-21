from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from posts.models import Post
from posts.permissions import IsPostAuthorOrReadOnly
from posts.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsPostAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
