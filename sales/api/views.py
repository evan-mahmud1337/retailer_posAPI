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
        today = datetime.now().date()
        yesterday= today - timedelta(days=1)
        print(yesterday)
        week= today - timedelta(weeks=7)
        months= today - timedelta(days=30)

        total_sale=Sale.objects.count()
        sale_yesterday=Sale.objects.filter(created_date=yesterday).count()
        sale_week=Sale.objects.filter(created_date__gte=week).count()
        sale_month=Sale.objects.filter(created_date__gte=months).count()

         # Retrieving total sale amounts for different time intervals
        sale_yesterday_amount = Sale.objects.filter(created_date=yesterday).aggregate(total_amount=Sum('total'))['total_amount']
        sale_week_amount = Sale.objects.filter(created_date__gte=week_start).aggregate(total_amount=Sum('total'))['total_amount']
        sale_month_amount = Sale.objects.filter(created_date__gte=month_start).aggregate(total_amount=Sum('total'))['total_amount']
        total_sale_amount = Sale.objects.aggregate(total_amount=Sum('total'))['total_amount']

         # If there are no sales for a particular period, set the total amount to 0
        sale_yesterday_amount = sale_yesterday_amount if sale_yesterday_amount else 0
        sale_week_amount = sale_week_amount if sale_week_amount else 0
        sale_month_amount = sale_month_amount if sale_month_amount else 0
        total_sale_amount = total_sale_amount if total_sale_amount else 0

        # Constructing response data
        response_data = {
            'total_sale': {
                'sale_month':sale_month
                'sale_week':sale_week,
                'sale_yesterday':sale_yesterday
                'total_sale':total_sale,
            },
            'total_sale_amount': {
                'monthly': sale_month_amount,
                'weekly': sale_week_amount,
                'yesterday': sale_yesterday_amount,
                'total': total_sale_amount
            }
        }
        
        # context={'total_sale':total_sale,'sale_yesterday':sale_yesterday,'sale_week':sale_week,
        #          'sale_month':sale_month}
        return Response(context, status=status.HTTP_200_OK)
