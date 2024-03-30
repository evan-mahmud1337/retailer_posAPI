from rest_framework import serializers
from inventory.models import *




class InventoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryCategory
        fields = ('__all__')

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ('__all__')

class VarientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Varient
        fields = ('__all__')