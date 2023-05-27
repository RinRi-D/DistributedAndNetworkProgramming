from concurrent.futures import ThreadPoolExecutor

import grpc
import calculator_pb2 as stub
import calculator_pb2_grpc as service

import math

SERVER_ADDR = '0.0.0.0:1234'

class Calculator(service.CalculatorServicer):
    def Add(self, request, context):
        a = request.a
        b = request.b
        print(f'Add({a}, {b})')
        return stub.FloatResponse(ans=a+b)

    def Substract(self, request, context):
        a = request.a
        b = request.b
        print(f'Substract({a}, {b})')
        return stub.FloatResponse(ans=a-b)

    def Multiply(self, request, context):
        a = request.a
        b = request.b
        print(f'Multiply({a}, {b})')
        return stub.FloatResponse(ans=a*b)

    def Divide(self, request, context):
        a = request.a
        b = request.b
        print(f'Divide({a}, {b})')
        try:
            return stub.FloatResponse(ans=a/b)
        except Exception as e:
            return stub.FloatResponse(ans=math.nan)


if __name__ == '__main__':
    try:
        server = grpc.server(ThreadPoolExecutor(max_workers=30))
        service.add_CalculatorServicer_to_server(Calculator(), server)
        server.add_insecure_port(SERVER_ADDR)
        server.start()
        print(f'listening on {SERVER_ADDR}')
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Interrupted by user. Shutting down...')
