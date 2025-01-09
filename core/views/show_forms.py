from core import serializers
from core.models import IncomeTracker
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class IncomeView(APIView):
    """
    Form for creating adding income for user
    """

    def get(self, request, *args, **kwargs):
        """
        Disply income form for user
        """
        incomes = IncomeTracker.objects.filter(user=request.user.id)
        serializer = serializers.IncomeSerializer(incomes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Add income from user
        """
        data = {
            'amount' : request.data["amount"],
            'source' : request.data['source'],
            'reason' : request.data['reason'],
            'remarks' : request.data['remarks'],
            'time' : request.data["time"]
        }
        serializer = serializers.IncomeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




