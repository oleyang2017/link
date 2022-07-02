# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import services.exhooks.exhook_pb2 as exhook__pb2


class HookProviderStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.OnProviderLoaded = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnProviderLoaded",
            request_serializer=exhook__pb2.ProviderLoadedRequest.SerializeToString,
            response_deserializer=exhook__pb2.LoadedResponse.FromString,
        )
        self.OnProviderUnloaded = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnProviderUnloaded",
            request_serializer=exhook__pb2.ProviderUnloadedRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnClientConnect = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnClientConnect",
            request_serializer=exhook__pb2.ClientConnectRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnClientConnack = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnClientConnack",
            request_serializer=exhook__pb2.ClientConnackRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnClientConnected = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnClientConnected",
            request_serializer=exhook__pb2.ClientConnectedRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnClientDisconnected = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnClientDisconnected",
            request_serializer=exhook__pb2.ClientDisconnectedRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnClientAuthenticate = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnClientAuthenticate",
            request_serializer=exhook__pb2.ClientAuthenticateRequest.SerializeToString,
            response_deserializer=exhook__pb2.ValuedResponse.FromString,
        )
        self.OnClientAuthorize = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnClientAuthorize",
            request_serializer=exhook__pb2.ClientAuthorizeRequest.SerializeToString,
            response_deserializer=exhook__pb2.ValuedResponse.FromString,
        )
        self.OnClientSubscribe = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnClientSubscribe",
            request_serializer=exhook__pb2.ClientSubscribeRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnClientUnsubscribe = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnClientUnsubscribe",
            request_serializer=exhook__pb2.ClientUnsubscribeRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnSessionCreated = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnSessionCreated",
            request_serializer=exhook__pb2.SessionCreatedRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnSessionSubscribed = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnSessionSubscribed",
            request_serializer=exhook__pb2.SessionSubscribedRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnSessionUnsubscribed = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnSessionUnsubscribed",
            request_serializer=exhook__pb2.SessionUnsubscribedRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnSessionResumed = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnSessionResumed",
            request_serializer=exhook__pb2.SessionResumedRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnSessionDiscarded = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnSessionDiscarded",
            request_serializer=exhook__pb2.SessionDiscardedRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnSessionTakeovered = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnSessionTakeovered",
            request_serializer=exhook__pb2.SessionTakeoveredRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnSessionTerminated = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnSessionTerminated",
            request_serializer=exhook__pb2.SessionTerminatedRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnMessagePublish = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnMessagePublish",
            request_serializer=exhook__pb2.MessagePublishRequest.SerializeToString,
            response_deserializer=exhook__pb2.ValuedResponse.FromString,
        )
        self.OnMessageDelivered = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnMessageDelivered",
            request_serializer=exhook__pb2.MessageDeliveredRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnMessageDropped = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnMessageDropped",
            request_serializer=exhook__pb2.MessageDroppedRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )
        self.OnMessageAcked = channel.unary_unary(
            "/emqx.exhook.v1.HookProvider/OnMessageAcked",
            request_serializer=exhook__pb2.MessageAckedRequest.SerializeToString,
            response_deserializer=exhook__pb2.EmptySuccess.FromString,
        )


class HookProviderServicer(object):
    """Missing associated documentation comment in .proto file."""

    def OnProviderLoaded(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnProviderUnloaded(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnClientConnect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnClientConnack(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnClientConnected(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnClientDisconnected(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnClientAuthenticate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnClientAuthorize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnClientSubscribe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnClientUnsubscribe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnSessionCreated(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnSessionSubscribed(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnSessionUnsubscribed(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnSessionResumed(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnSessionDiscarded(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnSessionTakeovered(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnSessionTerminated(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnMessagePublish(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnMessageDelivered(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnMessageDropped(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnMessageAcked(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_HookProviderServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "OnProviderLoaded": grpc.unary_unary_rpc_method_handler(
            servicer.OnProviderLoaded,
            request_deserializer=exhook__pb2.ProviderLoadedRequest.FromString,
            response_serializer=exhook__pb2.LoadedResponse.SerializeToString,
        ),
        "OnProviderUnloaded": grpc.unary_unary_rpc_method_handler(
            servicer.OnProviderUnloaded,
            request_deserializer=exhook__pb2.ProviderUnloadedRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnClientConnect": grpc.unary_unary_rpc_method_handler(
            servicer.OnClientConnect,
            request_deserializer=exhook__pb2.ClientConnectRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnClientConnack": grpc.unary_unary_rpc_method_handler(
            servicer.OnClientConnack,
            request_deserializer=exhook__pb2.ClientConnackRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnClientConnected": grpc.unary_unary_rpc_method_handler(
            servicer.OnClientConnected,
            request_deserializer=exhook__pb2.ClientConnectedRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnClientDisconnected": grpc.unary_unary_rpc_method_handler(
            servicer.OnClientDisconnected,
            request_deserializer=exhook__pb2.ClientDisconnectedRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnClientAuthenticate": grpc.unary_unary_rpc_method_handler(
            servicer.OnClientAuthenticate,
            request_deserializer=exhook__pb2.ClientAuthenticateRequest.FromString,
            response_serializer=exhook__pb2.ValuedResponse.SerializeToString,
        ),
        "OnClientAuthorize": grpc.unary_unary_rpc_method_handler(
            servicer.OnClientAuthorize,
            request_deserializer=exhook__pb2.ClientAuthorizeRequest.FromString,
            response_serializer=exhook__pb2.ValuedResponse.SerializeToString,
        ),
        "OnClientSubscribe": grpc.unary_unary_rpc_method_handler(
            servicer.OnClientSubscribe,
            request_deserializer=exhook__pb2.ClientSubscribeRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnClientUnsubscribe": grpc.unary_unary_rpc_method_handler(
            servicer.OnClientUnsubscribe,
            request_deserializer=exhook__pb2.ClientUnsubscribeRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnSessionCreated": grpc.unary_unary_rpc_method_handler(
            servicer.OnSessionCreated,
            request_deserializer=exhook__pb2.SessionCreatedRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnSessionSubscribed": grpc.unary_unary_rpc_method_handler(
            servicer.OnSessionSubscribed,
            request_deserializer=exhook__pb2.SessionSubscribedRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnSessionUnsubscribed": grpc.unary_unary_rpc_method_handler(
            servicer.OnSessionUnsubscribed,
            request_deserializer=exhook__pb2.SessionUnsubscribedRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnSessionResumed": grpc.unary_unary_rpc_method_handler(
            servicer.OnSessionResumed,
            request_deserializer=exhook__pb2.SessionResumedRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnSessionDiscarded": grpc.unary_unary_rpc_method_handler(
            servicer.OnSessionDiscarded,
            request_deserializer=exhook__pb2.SessionDiscardedRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnSessionTakeovered": grpc.unary_unary_rpc_method_handler(
            servicer.OnSessionTakeovered,
            request_deserializer=exhook__pb2.SessionTakeoveredRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnSessionTerminated": grpc.unary_unary_rpc_method_handler(
            servicer.OnSessionTerminated,
            request_deserializer=exhook__pb2.SessionTerminatedRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnMessagePublish": grpc.unary_unary_rpc_method_handler(
            servicer.OnMessagePublish,
            request_deserializer=exhook__pb2.MessagePublishRequest.FromString,
            response_serializer=exhook__pb2.ValuedResponse.SerializeToString,
        ),
        "OnMessageDelivered": grpc.unary_unary_rpc_method_handler(
            servicer.OnMessageDelivered,
            request_deserializer=exhook__pb2.MessageDeliveredRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnMessageDropped": grpc.unary_unary_rpc_method_handler(
            servicer.OnMessageDropped,
            request_deserializer=exhook__pb2.MessageDroppedRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
        "OnMessageAcked": grpc.unary_unary_rpc_method_handler(
            servicer.OnMessageAcked,
            request_deserializer=exhook__pb2.MessageAckedRequest.FromString,
            response_serializer=exhook__pb2.EmptySuccess.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "emqx.exhook.v1.HookProvider", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class HookProvider(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def OnProviderLoaded(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnProviderLoaded",
            exhook__pb2.ProviderLoadedRequest.SerializeToString,
            exhook__pb2.LoadedResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnProviderUnloaded(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnProviderUnloaded",
            exhook__pb2.ProviderUnloadedRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnClientConnect(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnClientConnect",
            exhook__pb2.ClientConnectRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnClientConnack(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnClientConnack",
            exhook__pb2.ClientConnackRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnClientConnected(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnClientConnected",
            exhook__pb2.ClientConnectedRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnClientDisconnected(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnClientDisconnected",
            exhook__pb2.ClientDisconnectedRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnClientAuthenticate(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnClientAuthenticate",
            exhook__pb2.ClientAuthenticateRequest.SerializeToString,
            exhook__pb2.ValuedResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnClientAuthorize(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnClientAuthorize",
            exhook__pb2.ClientAuthorizeRequest.SerializeToString,
            exhook__pb2.ValuedResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnClientSubscribe(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnClientSubscribe",
            exhook__pb2.ClientSubscribeRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnClientUnsubscribe(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnClientUnsubscribe",
            exhook__pb2.ClientUnsubscribeRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnSessionCreated(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnSessionCreated",
            exhook__pb2.SessionCreatedRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnSessionSubscribed(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnSessionSubscribed",
            exhook__pb2.SessionSubscribedRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnSessionUnsubscribed(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnSessionUnsubscribed",
            exhook__pb2.SessionUnsubscribedRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnSessionResumed(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnSessionResumed",
            exhook__pb2.SessionResumedRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnSessionDiscarded(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnSessionDiscarded",
            exhook__pb2.SessionDiscardedRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnSessionTakeovered(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnSessionTakeovered",
            exhook__pb2.SessionTakeoveredRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnSessionTerminated(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnSessionTerminated",
            exhook__pb2.SessionTerminatedRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnMessagePublish(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnMessagePublish",
            exhook__pb2.MessagePublishRequest.SerializeToString,
            exhook__pb2.ValuedResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnMessageDelivered(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnMessageDelivered",
            exhook__pb2.MessageDeliveredRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnMessageDropped(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnMessageDropped",
            exhook__pb2.MessageDroppedRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnMessageAcked(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/emqx.exhook.v1.HookProvider/OnMessageAcked",
            exhook__pb2.MessageAckedRequest.SerializeToString,
            exhook__pb2.EmptySuccess.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
