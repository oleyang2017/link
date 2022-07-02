import json
from concurrent import futures

import grpc
from loguru import logger
from google.protobuf import json_format
from services.tasks.emqx.task import on_published
from services.tasks.device.task import change_device_status
from services.exhooks.exhook_pb2 import (
    HookSpec,
    EmptySuccess,
    LoadedResponse,
    ValuedResponse,
    ClientSubscribeRequest,
)
from services.exhooks.exhook_pb2_grpc import (
    HookProviderServicer,
    add_HookProviderServicer_to_server,
)


class HookProvider(HookProviderServicer):
    def OnClientConnected(self, request, context):
        data = json.loads(json_format.MessageToJson(request))
        change_device_status.delay(data, True)
        return EmptySuccess()

    def OnClientDisconnected(self, request, context):
        data = json.loads(json_format.MessageToJson(request))
        change_device_status.delay(data, False)
        return EmptySuccess()

    def OnClientSubscribe(self, request, context):
        return ClientSubscribeRequest()

    def OnProviderLoaded(self, request, context):
        return LoadedResponse(
            hooks=[
                HookSpec(name=b"client.connected", topics=[]),
                HookSpec(name=b"client.disconnected", topics=[]),
                HookSpec(name=b"message.publish", topics=[]),
                HookSpec(name=b"message.acked", topics=[]),
            ]
        )

    def OnMessagePublish(self, request, context):
        try:
            data = json.loads(json_format.MessageToJson(request))
            # 上面的format会导致payload错误
            payload = str(request.message.payload, encoding="utf-8")
            data["message"]["payload"] = payload
            on_published.delay(data)
        except Exception:
            logger.exception("handle message publish failed")
        return ValuedResponse(type=0, bool_result=False, message=request.message)

    def OnMessageAcked(self, request, context):
        return EmptySuccess()

    def OnProviderUnloaded(self, request, context):
        return EmptySuccess()


def run_server(port=4010):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_HookProviderServicer_to_server(HookProvider(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"start grpc server: [::]:{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    run_server()
