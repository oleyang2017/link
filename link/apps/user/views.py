from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.wechat import code2openid

from .models import UserProfile as User
from .serializers import UserDetailSerializer


@api_view(["post"])
@authentication_classes(())
@permission_classes(())
def login_or_register_with_wx(request):
    """
    使用微信登录或注册

    """
    open_id, union_id = code2openid(request.data.get("code"))
    if open_id:
        try:
            user = User.objects.get(wx_open_id=open_id)
        except User.DoesNotExist:
            user = User(
                wx_open_id=open_id,
                wx_union_id=union_id,
            )
            user.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "uid": user.id,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
    raise APIException(detail="登录失败", code=500)


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserDetailSerializer
    queryset = User.objects

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id).all()
