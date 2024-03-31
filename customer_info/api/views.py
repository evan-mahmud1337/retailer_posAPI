from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from customer_info.models import *
from customer_info.api.serializer import *

# Create your views here.


class Customerview(APIView):
    def get(self,request,pk=None):
        if pk is not None:
            queryset=Customer_info.objects.get(id=pk)
            serializers=CustomerSerializer(queryset,many=False)
            return Response(serializers.data)

        queryset=Customer_info.objects.all()
        serializers=CustomerSerializer(queryset,many=True)
        return Response(serializers.data) 
    
    def post(self,request):
        serializers=SellerSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'msg':'created successful'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class Salesview(APIView):
    def get(self,request,pk=None):
        if pk is not None:
            queryset=Sales.objects.get(id=pk)
            serializers=SellerSerializer(queryset,many=False)
            return Response(serializers.data)

        queryset=Sales.objects.all()
        serializers=SellerSerializer(queryset,many=True)
        return Response(serializers.data) 
    
    def post(self,request):
        serializers=SellerSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'msg':'created successful'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
