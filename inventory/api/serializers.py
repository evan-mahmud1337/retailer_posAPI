from rest_framework import serializers
from inventory.models import InventoryCategory, InventoryItem

class InventoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryCategory
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
    category = InventoryCategorySerializer(read_only=True)

    class Meta:
        model = InventoryItem
        fields = '__all__'

