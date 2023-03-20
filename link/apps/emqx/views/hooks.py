from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from emqx.tasks import *


@api_view(["post"])
@authentication_classes(())
@permission_classes(())
def hooks(request):
    """
    文档地址：https://www.emqx.io/docs/zh/v4.4/advanced/webhook.htm
    EMQX WebHook
    处理设备上下线、消息发布、订阅、取消订阅等事件
    """
    action = request.data.get("action")
    if action == "client_connected":
        handle_client_status.delay(request.data)
    elif action == "client_disconnected":
        handle_client_status.delay(request.data)
    elif action == "message_publish":
        handle_publish.delay(request.data)
    elif action == "session_subscribed":
        handle_subscribe.delay(request.data)
    elif action == "session_unsubscribed":
        handle_subscribe.delay(request.data)
    return Response(status=HTTP_200_OK)
