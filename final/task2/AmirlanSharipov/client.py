import grpc
import calculator_pb2 as service
import calculator_pb2_grpc as stub

import random


def Add(a, b):
    args = service.Request(a=a, b=b)
    response = stub.Add(args)
    print(f"{a} + {b} = {response.ans}")


def Substract(a, b):
    args = service.Request(a=a, b=b)
    response = stub.Substract(args)
    print(f"{a} - {b} = {response.ans}")


def Multiply(a, b):
    args = service.Request(a=a, b=b)
    response = stub.Multiply(args)
    print(f"{a} * {b} = {response.ans}")


def Divide(a, b):
    args = service.Request(a=a, b=b)
    response = stub.Divide(args)
    print(f"{a} / {b} = {response.ans}")


if __name__ == '__main__':
    with grpc.insecure_channel('localhost:1234') as channel:
        stub = stub.CalculatorStub(channel)

        Add(10, 2)
        Substract(10, 2)
        Multiply(10, 2)
        Divide(10, 2)
        Divide(10, 0)
