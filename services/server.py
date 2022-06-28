from concurrent import futures

import grpc

from database.db import db
from database.models import Device
from exhooks.exhook_pb2 import (
    HookSpec,
    EmptySuccess,
    LoadedResponse,
    ValuedResponse,
    ClientSubscribeRequest,
)
from exhooks.exhook_pb2_grpc import HookProviderServicer, add_HookProviderServicer_to_server


class HookProvider(HookProviderServicer):
    def OnClientConnected(self, request, context):
        client_id = request.clientinfo.clientid
        device = db.session.query(Device).filter(Device.client_id == client_id).first()
        if device:
            device.status = True
            db.session.commit()

        return EmptySuccess()

    def OnClientDisconnected(self, request, context):
        client_id = request.clientinfo.clientid
        device = db.session.query(Device).filter(Device.client_id == client_id).first()
        if device:
            device.status = False
            db.session.commit()
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


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_HookProviderServicer_to_server(HookProvider(), server)
    server.add_insecure_port("[::]:4010")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    server()
