from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HelloView(APIView):
    def get(self, request):
        name = request.query_params.get('name', 'مهمان')
        return Response({"message": f"سلام {name}!"}, status=status.HTTP_200_OK)
