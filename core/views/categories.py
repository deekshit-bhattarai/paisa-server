from core import core_serializers
from rest_framework import permissions, status
from rest_framework.views import APIView

from core.mixins import CustomResponseMixin
from core.models import ExpenseCategory

class Categories(CustomResponseMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        print(f"Authenticated user {request.user}")
        if not request.user.is_authenticated:
            return self.return_response(
                success=False,
                message="Please login first",
                errors = "User is not authenticated",
                status = status.HTTP_403_FORBIDDEN
            )
        categories = ExpenseCategory.objects.filter(user=request.user)
        serializer = core_serializers.CategorySerializer(categories, many=True)
        print(serializer.data)
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

