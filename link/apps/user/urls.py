from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView, TokenObtainPairView

from .views import get_tmp_secret, login_or_register_with_wx

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/token/wx/", login_or_register_with_wx, name="token_wx"),
    path("auth/tmp_secret/", get_tmp_secret, name="tmp_secret"),
]
