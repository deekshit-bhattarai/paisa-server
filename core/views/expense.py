from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.views import APIView

from core import core_serializers
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
        id = kwargs.get('id', None)
        print(id)
        if id:
            expense = get_object_or_404(ExpenseTracker, pk=id, user=request.user)
            serializer = core_serializers.ExpenseSerializer(expense)
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

    def patch(self, request, *args, **kwargs):
        income_id = kwargs.get("id")
        breakpoint()
        expense_instance = get_object_or_404(ExpenseTracker, id=income_id, user=request.user)

        data = request.data
        serializer = core_serializers.IncomeSerializer(expense_instance, data=data, partial=True, context = { "request" : request})
        if serializer.is_valid():
            serializer.save()
            return self.return_response(
                success=True,
                message="Income updated successfully",
                data=serializer.data
            )
        return self.return_response(
            success=False,
            message="An error occured",
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, *args, **kwargs):
        expense_id = kwargs.get('id')
        expense_instance = get_object_or_404(ExpenseTracker, id=expense_id, user=request.user)

        expense_instance.delete()
        return self.return_response(
            success=True,
            message="Entry deleted successfully",
            status = status.HTTP_204_NO_CONTENT

        )


