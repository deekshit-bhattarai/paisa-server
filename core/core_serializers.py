from rest_framework import serializers

from core.models import IncomeTracker

class IncomeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    user = serializers.HiddenField(default = serializers.CurrentUserDefault)
    class Meta:
        model = IncomeTracker
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    pass

