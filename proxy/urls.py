from django.urls import path
from .views import ProxyDocsAPIView, HealthCheckAPIView

urlpatterns = [
    # path('<str:service>/<path:path>', ProxyAPIView.as_view(), name='proxy'),
    path('docs/<str:service>/', ProxyDocsAPIView.as_view(), name='proxy-docs'),
    path('health/', HealthCheckAPIView.as_view(), name='health-check'),

]
