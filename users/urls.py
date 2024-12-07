from django.urls import path
from .views import RegisterUserView, LoginUserView, RefreshTokenView, UserProfileView

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register_user"),
    path("login/", LoginUserView.as_view(), name="login_user"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh_token"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
]
