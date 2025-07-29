from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests


class ProxyDocsAPIView(APIView):
    def get(self, request, service):
        service_map = getattr(settings, 'SERVICE_MAP', {})
        if service not in service_map:
            return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

        url = f"{service_map[service]}/schema/"

        try:
            resp = requests.get(url, timeout=5)
            if 'application/json' in resp.headers.get('Content-Type', ''):
                data = resp.json()
            else:
                data = resp.text

            return Response(
                data=data,
                status=resp.status_code,
                content_type=resp.headers.get('Content-Type', 'application/json')
            )
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": "Service unavailable", "detail": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
            
class HealthCheckAPIView(APIView):
    def get(self, request):
        services = getattr(settings, 'SERVICE_MAP', {})
        results = {}

        for name, url in services.items():
            try:
                r = requests.get(url, timeout=2)
                if r.status_code == 200:
                    results[name] = "healthy"
                else:
                    results[name] = f"unhealthy ({r.status_code})"
            except Exception as e:
                results[name] = f"down ({str(e)})"

        return Response(results, status=status.HTTP_200_OK)
