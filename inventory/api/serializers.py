from rest_framework import serializers
from inventory.models import InventoryCategory, InventoryItem, Variant

class InventoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryCategory
        fields = '__all__'

class VarientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'


class InventoryItemSerializer(serializers.ModelSerializer):
    category = InventoryCategorySerializer(read_only=True)
    variants = VarientSerializer(many=True, source="variant_set")

    class Meta:
        model = InventoryItem
        fields = '__all__'
