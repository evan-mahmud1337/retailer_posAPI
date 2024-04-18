from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from inventory.models import *
from .serializers import *
from decimal import Decimal, InvalidOperation
from rest_framework.exceptions import ValidationError



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
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        inventory_items = InventoryItem.objects.all()
        serializer = InventoryItemSerializer(inventory_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        itemname = request.data.get('itemName')
        category_id = request.data.get('category')
        otherCost = Decimal(request.data.get('otherCost'))
        invImage = request.data.get('image', None)
        transportationCost = Decimal(request.data.get('transportationCost'))
        unit = request.data.get('unit')
        mrp = request.data.get('mrp')
        color = request.data.get('color')
        is_variant = request.data.get('is_variant', False)

        try:
            inventory_category = InventoryCategory.objects.get(id=category_id)
            inventoryCost = Decimal(request.data.get('inventoryCost'))
            productCost = otherCost + transportationCost + inventoryCost / int(unit)

            inventory = InventoryItem.objects.create(
                category=inventory_category,
                itemName=itemname,
                otherCost=otherCost,
                transportationCost=transportationCost,
                unit=unit,
                productCost=productCost,
                inventoryCost=inventoryCost,
                invImage=invImage,
                mrp=mrp,
                color=color,
                is_variant=is_variant,
            )

            unit_per_size = request.data.get('unit_per_size', None)
            if unit_per_size and is_variant:
                for size, units in unit_per_size.items():
                    Variant.objects.create(item=inventory, size=size, unit=units)

            return Response({'success': 'Successfully created inventory item'}, status=status.HTTP_201_CREATED)
        except (ValueError, InventoryCategory.DoesNotExist) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class InventoryDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            inventory_item = InventoryItem.objects.get(id=pk)
            serializer = InventoryItemSerializer(inventory_item)
            return Response(serializer.data)
        except InventoryItem.DoesNotExist:
            return Response({'error': 'Inventory item not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            inventory_item = InventoryItem.objects.filter(id=pk)
            unit = request.data.get('unit')

            # Validate unit type
            if not isinstance(unit, int):
                raise ValidationError({'unit': 'Unit must be an integer'})

            try:
                costs = {
                    'otherCost': Decimal(request.data.get('otherCost')),
                    'transportationCost': Decimal(request.data.get('transportationCost')),
                    'inventoryCost': Decimal(request.data.get("inventoryCost")),
                    'productCost': Decimal(request.data.get('productCost'))
                }
            except InvalidOperation as e:
                raise ValidationError({'error': 'Invalid decimal value: ' + str(e)})

            for field, value in costs.items():
                if value is None:
                    del costs[field]

            updated_fields = {'unit': int(unit)}
            updated_fields.update(costs)

            inventory_item.update(**updated_fields)
            return Response({'success': f"Stock updated, new stock {unit}"}, status=status.HTTP_200_OK)
        except InventoryItem.DoesNotExist:
            return Response({'error': 'Inventory item not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            inventory_item = InventoryItem.objects.get(id=pk)
            inventory_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InventoryItem.DoesNotExist:
            return Response({'error': 'Inventory item not found'}, status=status.HTTP_404_NOT_FOUND)


