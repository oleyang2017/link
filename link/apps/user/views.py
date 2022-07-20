from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.wechat import code2openid

from .models import UserProfile as User


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


@api_view(["get"])
def get_tmp_secret(request):
    config = {
        "duration_seconds": 7200,
        "secret_id": settings.T_CLOUD_SECRET_ID,
        "secret_key": settings.T_CLOUD_SECRET_KEY,
        "bucket": settings.T_CLOUD_BUCKET,
        "region": settings.T_CLOUD_REGION,
        "allow_prefix": f"{request.user.id}/*",
        "allow_actions": [
            # 简单上传
            "name/cos:PutObject",
            "name/cos:PostObject",
            # 分片上传
            "name/cos:InitiateMultipartUpload",
            "name/cos:ListMultipartUploads",
            "name/cos:ListParts",
            "name/cos:UploadPart",
            "name/cos:CompleteMultipartUpload",
        ],
    }
    sts = Sts(config=config)
    response = sts.get_credential()
    response["Bucket"] = settings.T_CLOUD_BUCKET
    response["Region"] = settings.T_CLOUD_REGION
    response["Prefix"] = f"{request.user.id}/"
    return Response(response)
