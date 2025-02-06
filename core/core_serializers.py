from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import ExpenseCategory, ExpenseTracker, IncomeTracker


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    class Meta:
        model = ExpenseCategory
        fields = '__all__'

class IncomeSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    category = serializers.SerializerMethodField()
    transaction_type = serializers.SerializerMethodField()
    class Meta:
        model = IncomeTracker
        fields = '__all__'

    def get_transaction_type(self, obj):
        return "Income"

    def get_category(self, obj):
        return None
        
class ExpenseSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    category = CategorySerializer()
    transaction_type = serializers.SerializerMethodField()
    class Meta:
        model = ExpenseTracker
        fields = ['id', 'transaction_type', 'category', 'amount', 'source', 'reason', 'remarks', 'time',  'user']

    def create(self, validated_data):
        category_name = validated_data.pop("category")

        print(f"Category name is {category_name}")

        if isinstance(category_name, int):
            category = ExpenseCategory.objects.get(id=category_name)
        else:
            category, _ = ExpenseCategory.objects.get_or_create(**category_name)
        expense = ExpenseTracker.objects.create(category = category, **validated_data)
        return expense

    def update(self, instance, validated_data):
        category_name = validated_data.pop("category", None)

        if category_name:
            instance.category.name = category_name.get("name", instance.category.name)
            instance.category.save()

        instance.amount = validated_data.get("amount", instance.amount)
        instance.source = validated_data.get("source", instance.source)
        instance.reason = validated_data.get("reason", instance.reason)
        instance.remarks = validated_data.get("remarks", instance.remarks)
        instance.time = validated_data.get("time", instance.time)
        instance.user = validated_data.get("user", instance.user)
        instance.save()
        return instance

    def get_transaction_type(self, obj):
        return "Expense"
