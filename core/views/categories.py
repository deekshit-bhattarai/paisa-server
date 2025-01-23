from core import core_serializers
from rest_framework import permissions
from rest_framework.views import APIView

from core.mixins import CustomResponseMixin
from core.models import ExpenseCategory

class Categories(CustomResponseMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        categories = ExpenseCategory.objects.filter(user=request.user)
        serializer = core_serializers.CategorySerializer(categories, many=True)
        return self.return_response(
            success=True,
            message="Got all categories",
            data=serializer.data
        )
        
    def post(self, request, *args, **kwargs):
        print(request)
        data = {
            'name' : request.data['name']
        }
        serializer = core_serializers.CategorySerializer(data=data, context={'request' : request})
        if serializer.is_valid():
            serializer.save()
            return self.return_response(
                success=True,
                message="Added category successfully",
                data=serializer.data
            )

