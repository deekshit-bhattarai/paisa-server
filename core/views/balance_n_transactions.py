from rest_framework import permissions
from rest_framework.views import APIView
from core import utils
from core.core_serializers import ExpenseSerializer, IncomeSerializer
from core.mixins import CustomResponseMixin
from core.models import ExpenseTracker, IncomeTracker

class CurrentBalance(CustomResponseMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_balance = utils.current_balance(request.user)
        return self.return_response(
            success=True,
            message="Successfully got current balance",
            data=current_balance,
        )

class RecentTransactions(CustomResponseMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        recent_transactions = utils.all_transactions(request.user).get('recent_transactions')
        return self.return_response(
            success=True,
            message="Recent transactions fetched successfully",
            data = recent_transactions
        )

class AllTransactions(CustomResponseMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        
        income_qs = IncomeTracker.objects.filter(user=user)
        expense_qs = ExpenseTracker.objects.filter(user=user).select_related('category')
        
        income_serialized = IncomeSerializer(income_qs, many=True).data
        expense_serialized = ExpenseSerializer(expense_qs, many=True).data

        # Combine and sort transactions by the 'time' field (latest first)
        combined = income_serialized + expense_serialized
        combined_sorted = sorted(combined, key=lambda x: x['time'], reverse=True)
        
        return self.return_response(
            success=True,
            message="Got all transactions successfully",
            data=combined_sorted
        )
