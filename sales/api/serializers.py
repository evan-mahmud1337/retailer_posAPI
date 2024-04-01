from rest_framework import serializers
from sales.models import Customer, Sale, SaleItem, SalesReturn

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ('id', 'item', 'quantity', 'size', 'item_name')
    item_name = serializers.SerializerMethodField()

    def get_item_name(self, obj):
        return obj.item.itemName


class SaleSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    saleitems = SaleItemSerializer(many=True, source='saleitem_set')

    class Meta:
        model = Sale
        fields = ('id', 'customer', 'vat_percentage', 'tax_percentage', 'discount_percentage',
                  'subtotal', 'total', 'delivery_cost', 'created_date', 'saleitems')


class SalesReturnSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    sale = SaleSerializer(read_only=True)
    sale_created_date = serializers.SerializerMethodField()
    sale_delivery_cost = serializers.SerializerMethodField()
    sale_total = serializers.SerializerMethodField()

    class Meta:
        model = SalesReturn
        fields = ('id', 'date', 'sale_created_date', 'sale_delivery_cost', 'sale_total', 'customer', 'sale')

    def get_sale_created_date(self, obj):
        sale = obj.sale
        return sale.created_date if sale else None

    def get_sale_delivery_cost(self, obj):
        sale = obj.sale
        return sale.delivery_cost if sale else None

    def get_sale_total(self, obj):
        sale = obj.sale
        return sale.total if sale else None