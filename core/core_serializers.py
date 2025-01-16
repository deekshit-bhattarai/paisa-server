from rest_framework import serializers

from core.models import ExpenseCategory, ExpenseTracker, IncomeTracker


class IncomeSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    class Meta:
        model = IncomeTracker
        fields = '__all__'
        
class ExpenseSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    class Meta:
        model = ExpenseTracker
        fields = ['amount', 'source', 'reason', 'category', 'remarks', 'time', 'user']

class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
