from concurrent import futures

import grpc
from loguru import logger
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
        logger.info(request)
        change_device_status.delay(request, True)
        return EmptySuccess()

    def OnClientDisconnected(self, request, context):
        logger.info(request)
        change_device_status.delay(request, False)
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
        return ValuedResponse(type=0, bool_result=False, message=request.message)

    def OnMessageAcked(self, request, context):
        return EmptySuccess()

    def OnProviderUnloaded(self, request, context):
        return EmptySuccess()


def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_HookProviderServicer_to_server(HookProvider(), server)
    server.add_insecure_port("[::]:4000")
    server.start()
    logger.info("start grpc server")
    server.wait_for_termination()


if __name__ == "__main__":
    run_server()
