from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework_simplejwt.tokens import RefreshToken
from utils.wechat import code2openid

from .models import UserProfile as User


@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def login_or_register_with_wx(request):
    """
    使用微信登录或注册
    """
    open_id = code2openid(request.data.get('code'))
    if open_id:
        try:
            user = User.objects.get(wx_open_id=open_id)
        except User.DoesNotExist:
            user = User(username=request.data.get('nickName'),
                        wx_open_id=open_id,
                        gender=request.data.get('gender'),
                        avatar_url=request.data.get('avatarUrl'))
            user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    raise APIException(detail='登录失败', code=500)


