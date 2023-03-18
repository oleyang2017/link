from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from device.models.device import Device
from user.models.user_profile import UserProfile as User


@api_view(["post"])
@authentication_classes(())
@permission_classes(())
def check_alc(request):
    """
    文档地址：https://www.emqx.io/docs/zh/v4.4/advanced/acl-http.html

    所有设备都通过 $save 主题上报数据，$cmd/[command_id] 主题接收命令，$resp/[command_id] 主题响应指令
    如果是设备订阅，那么主题为 $sub/[client_id]，其中 client_id 为被接收设备的 client_id
    需要校验用户是否有订阅权限
    docker-compose emqx environment:
      EMQX_AUTH__HTTP__ACL_REQ__METHOD: post
      EMQX_AUTH__HTTP__ACL_REQ__CONTENT_TYPE: json
      EMQX_AUTH__HTTP__ACL_REQ__PARAMS: access=%A,username=%u,topic=%t

    access: 1 为订阅，2 为发布
    """
    access = request.data.get("access")
    topic = request.data.get("topic")
    username = request.data.get("username")
    if access == "2" and (topic.startswith("$save") or topic.startswith("$resp")):
        return Response(status=HTTP_200_OK)
    if access == "1" and topic.startswith("$cmd"):
        return Response(status=HTTP_200_OK)
    if access == "1" and topic.startswith("$sub"):
        sub_client_id = topic.split("/")[1]
        user = User.objects.filter(emqx_user__username=username).first()
        device = Device.objects.filter(client_id=sub_client_id).first()
        if user and device:
            if user.has_perm("device.sub", device):
                return Response(status=HTTP_200_OK)
            else:
                return Response(status=HTTP_403_FORBIDDEN)
        else:
            return Response(status=HTTP_403_FORBIDDEN)
