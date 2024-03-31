from rest_framework import serializers
from customer_info.models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer_info
        fields=('id','name','number','address')


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sales
        fields=('id','product_id','product_varient','vat','tax','discount','price','delivery_cost','received_date')
