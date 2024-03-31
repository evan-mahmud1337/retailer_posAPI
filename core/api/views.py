from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from core.models import *
from .serializers import ExpenseSerializer, ExpenseCategorySerializer
from rest_framework import status



class ExpenseCategoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        expenseCategpries = ExpenseCategory.objects.all()
        serializer = ExpenseCategorySerializer(expenseCategpries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer = ExpenseCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        note = request.data.get('note', None)
        amount = request.data.get('amount', None)
        category_id = request.data.get('category', None)
        date  = request.data.get('date', None)
        try:
            category = ExpenseCategory.objects.get(id=category_id)
            expense = Expense.objects.create(category=category, amount=float(amount), note=note, date=date)
            expense.save()
            return Response({'success': 'successfully created'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'something went wrong{e}'}, status=status.HTTP_400_BAD_REQUEST)
