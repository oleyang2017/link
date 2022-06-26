import logging
from concurrent import futures

import grpc
import exhook_pb2
import exhook_pb2_grpc


class HookProvider(exhook_pb2_grpc.HookProviderServicer):
    def OnClientConnect(self, request, context):
        print(">>>>OnClientConnect")
        print(request)
        return exhook_pb2.EmptySuccess()

    def OnClientConnected(self, request, context):
        print(">>>>OnClientConnected")
        print(request)
        return exhook_pb2.EmptySuccess()

    def OnClientDisconnected(self, request, context):
        print(">>>>>dis")
        print(request)
        return exhook_pb2.EmptySuccess()

    def OnClientSubscribe(self, request, context):
        return exhook_pb2.ClientSubscribeRequest()

    def OnProviderLoaded(self, request, context):
        print("sss")
        return exhook_pb2.LoadedResponse(
            hooks=[
                exhook_pb2.HookSpec(name=b"client.connect", topics=[]),
                exhook_pb2.HookSpec(name=b"client.connected", topics=[]),
                exhook_pb2.HookSpec(name=b"client.disconnected", topics=[]),
                exhook_pb2.HookSpec(name=b"message.publish", topics=[]),
                exhook_pb2.HookSpec(name=b"message.acked", topics=[]),
            ]
        )

    def OnMessagePublish(self, request, context):
        print("publish")
        print(request)
        print("publish end")
        # 查询出这个topic的触发条件
        # 判断是否触发动作
        # 如果触发了，执行动作
        # action表结构设计
        # next_ids, need_callback
        return exhook_pb2.ValuedResponse(type=0, bool_result=False, message=request.message)

    def OnMessageAcked(self, request, context):
        print("ack")
        print(request)
        print("ack end")
        return exhook_pb2.EmptySuccess()

    def OnProviderUnloaded(self, request, context):
        return exhook_pb2.EmptySuccess()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    exhook_pb2_grpc.add_HookProviderServicer_to_server(HookProvider(), server)
    server.add_insecure_port("[::]:9000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    print(222)
    serve()
