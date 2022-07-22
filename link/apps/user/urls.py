from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView, TokenObtainPairView

from .views import UserViewSet, login_or_register_with_wx

router = DefaultRouter()
router.register("user", UserViewSet, basename="users")
urlpatterns = router.urls
urlpatterns += [
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/wx/login/", login_or_register_with_wx, name="token_wx"),
]
