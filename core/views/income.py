from django.shortcuts import get_object_or_404
from core import core_serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from core.mixins import CustomResponseMixin
from core.models import IncomeTracker


class IncomeView(CustomResponseMixin, APIView):
    """
    Form for creating adding income for user
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Disply income form for user
        """
        pk = kwargs.get('pk', None)
        print(pk)
        if pk:
            income = get_object_or_404(IncomeTracker, pk=pk, user=request.user)
            serializer = core_serializers.IncomeSerializer(income)
            return self.return_response(
                success=True,
                message="Got selected income successfully",
                data=serializer.data,
            )
        else:
            incomes = IncomeTracker.objects.filter(user=request.user)
            serializer = core_serializers.IncomeSerializer(incomes, many=True)
            data = serializer.data
            return self.return_response(
                success=True,
                message="Got all income successfully",
                data=data
            )

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
        serializer = core_serializers.IncomeSerializer( data=data, context={'request' : request} )
        print(request)
        if serializer.is_valid():
            serializer.save()
            return self.return_response(
                success=True,
                message="Income added successfully",
                data=serializer.data,
                status = status.HTTP_201_CREATED
            )

        return self.return_response(
            success=False,
            message="An error occured",
            data=serializer.errors,
            status = status.HTTP_201_CREATED
        )




