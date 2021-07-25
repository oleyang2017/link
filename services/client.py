from __future__ import print_function
import logging

import grpc

import exhook_pb2
import exhook_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:9000') as channel:
        stub = exhook_pb2_grpc.HookProviderStub(channel)
        response = stub.OnClientConnect(exhook_pb2.ClientConnectRequest())
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()