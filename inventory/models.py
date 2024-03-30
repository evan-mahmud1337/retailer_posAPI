from django.db import models
from django.contrib.auth import get_user_model


class InventoryCategory(models.Model):
    name = models.CharField(max_length=50)
    additionalInfo = models.TextField(max_length=256, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class InventoryItem(models.Model):
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=100)
    unit = models.PositiveIntegerField()
    transportationCost = models.PositiveIntegerField()
    otherCost = models.PositiveIntegerField()
    invImage = models.ImageField(upload_to=f'inventory/', blank=True)
    isVarient = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.itemName
    
class Varient(models.Model):
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large')
    )
    inv = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    size = models.CharField(choices=sizes, max_length=100)
    unit = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.color} {self.size}"
class Color(models.Model):
    varient = models.ForeignKey(Varient, on_delete=models.CASCADE)
    color = models.CharField(max_length=30)
    unit = models.PositiveIntegerField()

    def __str__(self):
        return f"Varient {self.varient.size} color {self.color}"

