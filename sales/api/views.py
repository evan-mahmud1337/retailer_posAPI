from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from sales.models import *
from .serializers import CustomerSerializer, SaleSerializer
from django.db import transaction
from datetime import datetime,timedelta

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
                inventory_item = InventoryItem.objects.get(id=item_data['id'])
                inventory_item.unit -= item_data['quantity']
                inventory_item.save()

                SaleItem.objects.create(
                    sale=sale,
                    item_id=inventory_item.id,
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

class DashboardView(APIView):
    
    def get(self, request, format=None):
        yesterday=datetime.now().date()-timedelta(days=1)
        print(yesterday)
        week=datetime.now().date()-timedelta(weeks=1)
        months=datetime.now().date()-timedelta(days=30)

        total_sale=Sale.objects.count()
        sale_yesterday=Sale.objects.filter(created_date=yesterday).count()
        sale_week=Sale.objects.filter(created_date__gte=week).count()
        sale_month=Sale.objects.filter(created_date__gte=months).count()
        
        context={'total_sale':total_sale,'sale_yesterday':sale_yesterday,'sale_week':sale_week,
                 'sale_month':sale_month}
        return Response(context, status=status.HTTP_200_OK)
