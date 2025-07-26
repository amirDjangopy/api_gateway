from django.urls import path
from .views import GRPCProxyView

urlpatterns = [
    path('proxy/<str:service_key>/<str:method_name>/', GRPCProxyView.as_view(), name='grpc-proxy'),
]
