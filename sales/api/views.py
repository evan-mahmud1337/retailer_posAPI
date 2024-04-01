from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from sales.models import *
from .serializers import CustomerSerializer, SaleSerializer, SalesReturnSerializer
from django.db import transaction

class SaleCreateView(APIView):
    def get(self, request, format=None):
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        customer_data = request.data.get('customer')
        saleitems_data = request.data.get('saleitems')

        customer, created = Customer.objects.get_or_create(**customer_data)

        with transaction.atomic():
            sale_data = {
                'customer': customer,
                'vat_percentage': request.data.get('vat_percentage'),
                'tax_percentage': request.data.get('tax_percentage'),
                'discount_percentage': request.data.get('discount_percentage'),
                'subtotal': request.data.get('subtotal'),
                'total': request.data.get('total'),
                'delivery_cost': request.data.get('delivery_cost'),
            }
            sale = Sale.objects.create(**sale_data)

            for item_data in saleitems_data:
                inventory_item = InventoryItem.objects.get(id=int(item_data['id']))

                if inventory_item is None:
                    raise ValueError("The field 'unit' is likely intended for available quantity. Rename it to 'quantity' or 'available_quantity'.")

                new_quantity = inventory_item.unit - item_data['quantity']
                if new_quantity >= 0:
                    inventory_item.unit = new_quantity
                    inventory_item.save()
                else:
                    raise ValueError("Insufficient stock for sale. Item ID: " + str(inventory_item.id))

                SaleItem.objects.create(
                    sale=sale,
                    item=inventory_item,
                    quantity=item_data['quantity'],
                    size=item_data.get('size')
                )

        serializer = SaleSerializer(sale)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class SaleRetrieveView(APIView):
    def get(self, request, pk):
        try:
            print(pk)
            sale = Sale.objects.get(pk=pk)
            serializer = SaleSerializer(sale)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Sale.DoesNotExist:
            return Response({'error': 'Sale not found'}, status=status.HTTP_404_NOT_FOUND)
        
class SalesReturnView(APIView):
    def get(self, request, format=None):
        sale_returns = SalesReturn.objects.all()
        serializer = SalesReturnSerializer(sale_returns, many=True)
        return  Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        sale_id = request.data.get('sale_id', None)
        reason = request.data.get('reason', None)

        try:
            sale = Sale.objects.get(id=sale_id)
        except Sale.DoesNotExist:
            return Response({'error': 'Invalid sale ID provided'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            sales_return = SalesReturn.objects.create(sale=sale, reason=reason)

            for sale_item in sale.saleitem_set.all():
                inventory_item = InventoryItem.objects.get(id=sale_item.item_id)
                inventory_item.unit += sale_item.quantity
                inventory_item.save()  # Update inventory

            serializer = SalesReturnSerializer(sales_return)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


