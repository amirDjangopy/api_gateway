from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .grpc_clients.client import GRPCClient

def grpc_message_to_dict(message):
    """ 
    Convert gRPC response to dictionary recursively 
    """
    
    if message is None:
        return {}
    if hasattr(message, 'ListFields'):
        result = {}
        for field, value in message.ListFields():
            if hasattr(value, 'ListFields'):
                result[field.name] = grpc_message_to_dict(value)
            elif isinstance(value, (list, tuple)):
                result[field.name] = [grpc_message_to_dict(v) if hasattr(v, 'ListFields') else v for v in value]
            else:
                result[field.name] = value
        return result
    return message

class GRPCProxyView(APIView):
    """
    Proxy for forwarding requests to gRPC services
    """
    
    def post(self, request, service_key, method_name):
        service_map = settings.SERVICE_MAP

        if service_key not in service_map:
            return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

        service_info = service_map[service_key]
        grpc_client = GRPCClient(service_info['service_name'], service_info['address'])

        request_data = request.data

        try:
            grpc_response = grpc_client.call_method(method_name, request_data)
            response_dict = grpc_message_to_dict(grpc_response)
            return Response(response_dict)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
