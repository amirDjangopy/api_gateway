import grpc
import importlib

class GRPCClient:
    def __init__(self, service_name, address):
        """
        service_name: str, مثلاً 'service1' یا 'service2'
        address: آدرس سرویس gRPC مثل 'localhost:50051'
        """
        self.service_name = service_name
        self.address = address
        self.channel = grpc.insecure_channel(self.address)

        # import dynamic proto modules
        pb2_grpc_module = importlib.import_module(f".proto.{service_name}_pb2_grpc", package="gateway_app.grpc_clients")
        pb2_module = importlib.import_module(f".proto.{service_name}_pb2", package="gateway_app.grpc_clients")

        # استخراج Stub class از ماژول
        stub_class_name = None
        for attr in dir(pb2_grpc_module):
            if attr.endswith('Stub'):
                stub_class_name = attr
                break
        if not stub_class_name:
            raise Exception(f"Stub class not found in {service_name}_pb2_grpc.py")

        stub_class = getattr(pb2_grpc_module, stub_class_name)
        self.stub = stub_class(self.channel)
        self.pb2 = pb2_module

    def call_method(self, method_name, request_data):
        """
        method_name: نام متدی که در gRPC میخوای صدا بزنی
        request_data: دیکشنری ورودی که باید به Message تبدیل بشه

        دقت کن اینجا فقط نمونه ساده‌س و برای پیام‌های ساده به کار میره.
        """
        if not hasattr(self.stub, method_name):
            raise Exception(f"Method {method_name} not found in {self.service_name} Stub")

        method = getattr(self.stub, method_name)

        # ساخت پیام درخواست از دیکشنری (نیاز به تطبیق دقیق فیلدها داره)
        request_message = self.pb2.__dict__[method_name + "Request"]()  # فرض بر اینه پیام درخواست اسمش مثل MethodNameRequest هست
        for k, v in request_data.items():
            setattr(request_message, k, v)

        response = method(request_message)
        return response
