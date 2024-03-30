from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from inventory.models import *
from .serializers import *



class InventoryCategoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        invetnoryCategory = InventoryCategory.objects.all()
        serializer = InventoryCategorySerializer(invetnoryCategory,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = InventoryCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class InventoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        inventory_items = InventoryItem.objects.all()
        serializer = InventoryItemSerializer(inventory_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InventoryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            inventory_item = InventoryItem.objects.get(pk=pk)
            serializer = InventoryItemSerializer(inventory_item)
            return Response(serializer.data)
        except InventoryItem.DoesNotExist:
            return Response({'error': 'Inventory item not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            inventory_item = InventoryItem.objects.get(pk=pk)
            serializer = InventoryItemSerializer(inventory_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InventoryItem.DoesNotExist:
            return Response({'error': 'Inventory item not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            inventory_item = InventoryItem.objects.get(pk=pk)
            inventory_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InventoryItem.DoesNotExist:
            return Response({'error': 'Inventory item not found'}, status=status.HTTP_404_NOT_FOUND)


