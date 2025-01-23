from django.shortcuts import get_object_or_404
from core import core_serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from core.mixins import CustomResponseMixin
from core.models import ExpenseTracker


class ExpenseView(CustomResponseMixin, APIView):
    """
    Form for creating adding expense for user
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Disply expense form for user
        """
        pk = kwargs.get('pk', None)
        print(pk)
        if pk:
            expense = get_object_or_404(ExpenseTracker, pk=pk, user=request.user)
            serializer = core_serializers.IncomeSerializer(expense)
            return self.return_response(
                success=True,
                message = "Got selected expense successfully",
                data = serializer.data
            )
        # breakpoint()
        else:
            expenses = ExpenseTracker.objects.filter(user=request.user)
            serializer = core_serializers.ExpenseSerializer(expenses, many=True)
            data = serializer.data
            return self.return_response(
                success=True,
                message = "Filtered expense successfully",
                data = data
            )

    def post(self, request, *args, **kwargs):
        """
        Add expense from user
        """
        # breakpoint()
        data = {
            'amount' : request.data["amount"],
            'source' : request.data['source'],
            'reason' : request.data['reason'],
            'remarks' : request.data['remarks'],
            'category': request.data['category'],
            'time' : request.data["time"],
            'user': request.user
        }
        serializer = core_serializers.ExpenseSerializer( data=data, context={'request' : request} )
        print(request)
        if serializer.is_valid():
            serializer.save()
            return self.return_response(
                success=True,
                message="Added expense successfully", 
                data=serializer.data,
                status = status.HTTP_201_CREATED
            )

        return self.return_response(
            success=False,
            message="An error occured",
            errors = {'error' : serializer.errors},
            status = status.HTTP_400_BAD_REQUEST
        )




