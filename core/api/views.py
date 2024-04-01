from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from core.models import *
from .serializers import ExpenseSerializer
from rest_framework import status
from permission.permissions import *


class ExpenseCategoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsManagerOrAbove]

    def get(self, request, format=None):
        expenseCategpries = ExpenseCategory.objects.all()
        serializer = ExpenseSerializer(expenseCategpries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsManagerOrAbove]

    def get(self, request):
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
