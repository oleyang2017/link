from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from device.models.device import Device


@api_view(["post"])
@authentication_classes(())
@permission_classes(())
def check_auth(request):
    """
    文档地址：https://www.emqx.io/docs/zh/v4.4/advanced/auth-http.html
    docker-compose emqx environment:
      EMQX_AUTH__HTTP__ACL_REQ__METHOD: post
      EMQX_AUTH__HTTP__ACL_REQ__CONTENT_TYPE: json
      EMQX_AUTH__HTTP__ACL_REQ__PARAMS: client_id=%c,username=%u,password=%P
    """
    username = request.data.get("username")
    password = request.data.get("password")
    client_id = request.data.get("client_id")
    device = Device.objects.filter(
        client_id=client_id,
        create_user__emqx_user__username=username,
        create_user__emqx_user__password=password,
    ).first()
    if device:
        return Response(status=HTTP_200_OK)
    else:
        return Response(status=HTTP_401_UNAUTHORIZED)
