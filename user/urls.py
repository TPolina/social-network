from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from user.views import CreateUserView, RetrieveUpdateUserView, UserActivityView

urlpatterns = [
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("profile/", RetrieveUpdateUserView.as_view(), name="profile"),
    path("activity/", UserActivityView.as_view(), name="activity"),
]

app_name = "user"
