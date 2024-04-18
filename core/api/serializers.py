from rest_framework import serializers

from core.models import Expense, ExpenseCategory

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'additionalInfo']

class ExpenseSerializer(serializers.ModelSerializer):
    category = ExpenseCategorySerializer(read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'note', 'date']

