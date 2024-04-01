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
    inventoryCost = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    productCost = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    transportationCost = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    otherCost = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    invImage = models.ImageField(upload_to=f'inventory/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.itemName
