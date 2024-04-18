from django.db import models
from django.contrib.auth import get_user_model


class InventoryCategory(models.Model):
    name = models.CharField(max_length=50)
    additionalInfo = models.TextField(max_length=256, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class InventoryItem(models.Model):
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=100)
    unit = models.PositiveIntegerField()
    inventoryCost = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    productCost = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    transportationCost = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    otherCost = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    invImage = models.ImageField(upload_to=f'inventory/', blank=True, null=True)
    is_variant = models.BooleanField(blank=True, null=True, default=False)
    color = models.CharField(max_length=200, blank=True, null=True)
    mrp = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.itemName

class Variant(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="variant_set")
    size = models.CharField(max_length=20)
    unit = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.item.itemName} - {self.size}'