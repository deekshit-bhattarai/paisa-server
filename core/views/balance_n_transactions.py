from rest_framework import permissions
from rest_framework.views import APIView
from core import utils
from core.mixins import CustomResponseMixin

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
