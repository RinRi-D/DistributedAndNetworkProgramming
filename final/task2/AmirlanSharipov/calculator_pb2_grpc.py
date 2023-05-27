# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import calculator_pb2 as calculator__pb2


class CalculatorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Add = channel.unary_unary(
                '/Calculator/Add',
                request_serializer=calculator__pb2.Request.SerializeToString,
                response_deserializer=calculator__pb2.FloatResponse.FromString,
                )
        self.Substract = channel.unary_unary(
                '/Calculator/Substract',
                request_serializer=calculator__pb2.Request.SerializeToString,
                response_deserializer=calculator__pb2.FloatResponse.FromString,
                )
        self.Multiply = channel.unary_unary(
                '/Calculator/Multiply',
                request_serializer=calculator__pb2.Request.SerializeToString,
                response_deserializer=calculator__pb2.FloatResponse.FromString,
                )
        self.Divide = channel.unary_unary(
                '/Calculator/Divide',
                request_serializer=calculator__pb2.Request.SerializeToString,
                response_deserializer=calculator__pb2.FloatResponse.FromString,
                )


class CalculatorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Add(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Substract(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Multiply(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Divide(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CalculatorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Add': grpc.unary_unary_rpc_method_handler(
                    servicer.Add,
                    request_deserializer=calculator__pb2.Request.FromString,
                    response_serializer=calculator__pb2.FloatResponse.SerializeToString,
            ),
            'Substract': grpc.unary_unary_rpc_method_handler(
                    servicer.Substract,
                    request_deserializer=calculator__pb2.Request.FromString,
                    response_serializer=calculator__pb2.FloatResponse.SerializeToString,
            ),
            'Multiply': grpc.unary_unary_rpc_method_handler(
                    servicer.Multiply,
                    request_deserializer=calculator__pb2.Request.FromString,
                    response_serializer=calculator__pb2.FloatResponse.SerializeToString,
            ),
            'Divide': grpc.unary_unary_rpc_method_handler(
                    servicer.Divide,
                    request_deserializer=calculator__pb2.Request.FromString,
                    response_serializer=calculator__pb2.FloatResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Calculator', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Calculator(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Add(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Calculator/Add',
            calculator__pb2.Request.SerializeToString,
            calculator__pb2.FloatResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Substract(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Calculator/Substract',
            calculator__pb2.Request.SerializeToString,
            calculator__pb2.FloatResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Multiply(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Calculator/Multiply',
            calculator__pb2.Request.SerializeToString,
            calculator__pb2.FloatResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Divide(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Calculator/Divide',
            calculator__pb2.Request.SerializeToString,
            calculator__pb2.FloatResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
