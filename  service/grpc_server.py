import grpc
from concurrent import futures
from app.grpc import hello_pb2_grpc
from app.grpc.services import HelloService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    server.add_insecure_port('0.0.0.0:5050') 
    print("🚀 gRPC server started on port 5050")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
