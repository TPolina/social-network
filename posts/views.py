from datetime import datetime

from django.db.models import Count
from django.db.models.functions import TruncDay
from rest_framework import viewsets, status, generics
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


class AnalyticsView(generics.GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            date_from = datetime.strptime(
                self.request.query_params.get("date_from"), "%Y-%m-%d"
            )
            date_to = datetime.strptime(
                self.request.query_params.get("date_to"), "%Y-%m-%d"
            )
        except (TypeError, ValueError):
            return

        return Like.objects.filter(
            created_at__range=(date_from, date_to)
        ).annotate(
            day=TruncDay("created_at")
        ).values("day").annotate(likes=Count("id"))

    def get(self, request):
        queryset = self.get_queryset()

        if queryset is None:
            return Response(
                {"detail": "Invalid date format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        analytics_data = [
            {"day": entry["day"].strftime("%Y-%m-%d"), "likes": entry["likes"]}
            for entry in queryset
        ]

        if not analytics_data:
            return Response(
                {"detail": "No likes during this period"},
                status=status.HTTP_200_OK
            )

        return Response(analytics_data, status=status.HTTP_200_OK)
