import grpc
from app.grpc import hello_pb2, hello_pb2_grpc  

def run():
    channel = grpc.insecure_channel('127.0.0.1:5050')
    stub = hello_pb2_grpc.HelloServiceStub(channel)

    request = hello_pb2.HelloRequest(name="علی")
    response = stub.SayHello(request)

    print("پیام سرور:", response.message)

if __name__ == "__main__":
    run()
