from django.urls import path, include
from rest_framework import routers

from posts.views import PostViewSet, AnalyticsView

router = routers.DefaultRouter()
router.register("posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("analytics/", AnalyticsView.as_view(), name="analytics"),
]

app_name = "posts"
