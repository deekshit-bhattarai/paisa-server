from core import core_serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import ExpenseCategory


class AddCategory(APIView):
    def get(self, request, *args, **kwargs):
        breakpoint()
        categories = ExpenseCategory.objects.filter(user=request.user)
        serializer = core_serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, *args, **kwargs):
        print(request)
        breakpoint()
        data = {
            'name' : request.data['name']
        }
        serializer = core_serializers.CategorySerializer(data=data, context={'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

