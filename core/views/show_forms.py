from core import core_serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from core.models import IncomeTracker


class IncomeView(APIView):
    """
    Form for creating adding income for user
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Disply income form for user
        """
        breakpoint()
        incomes = IncomeTracker.objects.filter(user=request.user.id)
        serializer = core_serializers.IncomeSerializer(incomes, many=True, context={'user' : request.user})
        data = serializer.data
        return Response({'data' : data})

    def post(self, request, *args, **kwargs):
        """
        Add income from user
        """
        # breakpoint()
        data = {
            'amount' : request.data["amount"],
            'source' : request.data['source'],
            'reason' : request.data['reason'],
            'remarks' : request.data['remarks'],
            'time' : request.data["time"],
            'user': request.user.id
        }
        serializer = core_serializers.IncomeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




