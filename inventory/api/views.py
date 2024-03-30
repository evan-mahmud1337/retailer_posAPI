from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from inventory.models import *
from  .serializers import *
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class InventoryCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        allInventory = InventoryCategory.objects.all()
        serializer = InventoryCategorySerializer(allInventory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def  post(self,request):
        cat_name = request.data.get('name', None)
        additionalInfo = request.data.get('additionalInfo', None)
        try:
            category = InventoryCategory.objects.create(name=cat_name, additionalInfo=additionalInfo)
            category.save()
            data = {
                'success': f"inventory category created with id {category.id}"
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        except  Exception as e:
            data = {'error': f'Error creating new category - {e}'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        

class InventoryItem(APIView):
    def get_item(self, itemId):
        try:
            item = InventoryItem.objects.get(pk=itemId)
            return item
        except InventoryItem.DoesNotExist:
            return None

    # Get All Items in the system
    def get(self, request, format=None):
        items = InventoryItem.objects.all().order_by("-dateAdded")
        serializedItems = InventoryItemSerializer(items, many=True)
        return Response(serializedItems.data, status=status.HTTP_200_OK)

    def post(self, request):
        # data of inventory
        itemName = request.data.get('name')
        unit = request.data.get('unit')
        transportationCost = request.data.get('transportationCost')
        otherCost = request.data.get('otherCost')
        invImage = request.data.get('invImage')
        isVarient = request.data.get('isVarient')
        categoryId = request.data.get('categoryId')

        # data of varient
        size = request.data.get('size', None)
        color = request.data.get('color', None)
        weight = request.data.get('weight', None)
        try:
            inventory = InventoryItem.objects.create(   category__id=categoryId,
                                                        itemName=itemName, unit=unit,
                                                        transportationCost=transportationCost,
                                                        otherCost=otherCost, invImage=invImage,
                                                        isVarient=isVarient,
                                                    )
            inventory.save()
            varient = Varient.objects.create(
                size=size,
            )
        except Exception as e:
            return f"Inventory item couldn't created {e}"