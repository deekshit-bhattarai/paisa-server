from rest_framework import permissions, status
from rest_framework.views import APIView, Response
from core import utils

class CurrentBalance(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_balance = utils.current_balance(request.user)
        return Response({'current_balance' : current_balance }, status=status.HTTP_200_OK)
