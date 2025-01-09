from rest_framework import serializers

from core.models import IncomeTracker

class IncomeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = IncomeTracker
        exclude = [ 'user' ]

class UserSerializer(serializers.ModelSerializer):
    pass

