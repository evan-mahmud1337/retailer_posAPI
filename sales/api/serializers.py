from rest_framework import serializers
from sales.models import Customer, Sale, SaleItem

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
