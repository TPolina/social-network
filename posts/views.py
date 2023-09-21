from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from posts.models import Post, Like
from posts.permissions import IsPostAuthorOrReadOnly
from posts.serializers import PostSerializer, LikeSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsPostAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("like_post", "unlike_post"):
            return LikeSerializer

        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="like",
        permission_classes=[IsAuthenticated],
    )
    def like_post(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like = Like.objects.filter(user=user, post=post).first()

        if not like:
            new_like = Like.objects.create(post=post, user=user)
            serializer = self.get_serializer(new_like, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"detail": "Post is already liked"},
            status=status.HTTP_409_CONFLICT
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="unlike",
        permission_classes=[IsAuthenticated],
    )
    def unlike_post(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like = Like.objects.filter(user=user, post=post).first()

        if like:
            like.delete()
            return Response(
                {"detail": "Post is unliked"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "Post wasn't liked"},
            status=status.HTTP_409_CONFLICT
        )
