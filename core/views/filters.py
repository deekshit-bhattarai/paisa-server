from rest_framework import permissions
from rest_framework.views import APIView

from core.core_serializers import ExpenseSerializer, IncomeSerializer
from core.mixins import CustomResponseMixin
from core.models import ExpenseTracker, IncomeTracker


class IncomeFilter(CustomResponseMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = IncomeTracker.objects.filter(user=request.user)

        source = request.query_params.get('source', None)
        category = request.query_params.get('category', None)
        time_from = request.query_params.get('from', None)
        time_to = request.query_params.get('to', None)

        if source:
            queryset = queryset.filter(source__iexact=source)
        if category:
            queryset = queryset.filter(category=category)
        if time_from and time_to:
            queryset = queryset.filter(time__range=[time_from, time_to])
        elif time_from:
            queryset = queryset.filter(time__gte=time_from)
        elif time_to:
            queryset = queryset.filter(time__lte=time_to)

        serializer = IncomeSerializer(queryset, many=True)
        return self.return_response(
            success=True,
            message="Filtered income successfully",
            data=serializer.data
        )

class ExpenseFilter(CustomResponseMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = ExpenseTracker.objects.filter(user=request.user)

        source = request.query_params.get('source', None)
        category = request.query_params.get('category', None)
        time_from = request.query_params.get('from', None)
        time_to = request.query_params.get('to', None)

        if source:
            queryset = queryset.filter(source__iexact=source)
        if category:
            queryset = queryset.filter(category=category)
        if time_from and time_to:
            queryset = queryset.filter(time__range=[time_from, time_to])
        elif time_from:
            queryset = queryset.filter(time__gte=time_from)
        elif time_to:
            queryset = queryset.filter(time__lte=time_to)

        serializer = ExpenseSerializer(queryset, many=True)
        return self.return_response(
            success=True,
            message="Filtered expense successfully",
            data=serializer.data
        )
