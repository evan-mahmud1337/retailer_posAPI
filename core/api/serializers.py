from rest_framework import serializers
from core.models import *

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'additionalInfo']

class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ExpenseCategory.objects.all())

    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'note', 'date']
