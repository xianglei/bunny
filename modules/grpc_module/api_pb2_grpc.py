# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import modules.grpc_module.api_pb2 as api__pb2


class ExecServiceStub(object):
    """exec service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Exec = channel.unary_unary(
                '/runtime.v1.grpc.api.ExecService/Exec',
                request_serializer=api__pb2.ExecRequest.SerializeToString,
                response_deserializer=api__pb2.ExecResponse.FromString,
                )
        self.StreamExec = channel.unary_stream(
                '/runtime.v1.grpc.api.ExecService/StreamExec',
                request_serializer=api__pb2.ExecRequest.SerializeToString,
                response_deserializer=api__pb2.ExecStreamResponse.FromString,
                )


class ExecServiceServicer(object):
    """exec service
    """

    def Exec(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamExec(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ExecServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Exec': grpc.unary_unary_rpc_method_handler(
                    servicer.Exec,
                    request_deserializer=api__pb2.ExecRequest.FromString,
                    response_serializer=api__pb2.ExecResponse.SerializeToString,
            ),
            'StreamExec': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamExec,
                    request_deserializer=api__pb2.ExecRequest.FromString,
                    response_serializer=api__pb2.ExecStreamResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'runtime.v1.grpc.api.ExecService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ExecService(object):
    """exec service
    """

    @staticmethod
    def Exec(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/runtime.v1.grpc.api.ExecService/Exec',
            api__pb2.ExecRequest.SerializeToString,
            api__pb2.ExecResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StreamExec(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/runtime.v1.grpc.api.ExecService/StreamExec',
            api__pb2.ExecRequest.SerializeToString,
            api__pb2.ExecStreamResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class HeartbeatServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Heartbeat = channel.unary_unary(
                '/runtime.v1.grpc.api.HeartbeatService/Heartbeat',
                request_serializer=api__pb2.HeartbeatRequest.SerializeToString,
                response_deserializer=api__pb2.HeartbeatResponse.FromString,
                )


class HeartbeatServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Heartbeat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HeartbeatServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Heartbeat': grpc.unary_unary_rpc_method_handler(
                    servicer.Heartbeat,
                    request_deserializer=api__pb2.HeartbeatRequest.FromString,
                    response_serializer=api__pb2.HeartbeatResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'runtime.v1.grpc.api.HeartbeatService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class HeartbeatService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Heartbeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/runtime.v1.grpc.api.HeartbeatService/Heartbeat',
            api__pb2.HeartbeatRequest.SerializeToString,
            api__pb2.HeartbeatResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
