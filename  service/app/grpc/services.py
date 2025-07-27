
from app.grpc import hello_pb2_grpc, hello_pb2

class HelloService(hello_pb2_grpc.HelloServiceServicer):
    def SayHello(self, request, context):
        name = request.name
        return hello_pb2.HelloReply(message=f"سلام {name}!")
