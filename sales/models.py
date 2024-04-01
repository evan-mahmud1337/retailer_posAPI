from django.db import models
import uuid
from inventory.models import InventoryItem


class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Sale #{self.id} - {self.customer.name}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='saleitem_set')
    quantity = models.PositiveIntegerField()
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity}x {self.item.name} ({self.size} size)"


class SalesReturn(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name= 'returns_set')
    reason = models.TextField(blank=True, null=True, max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"Return for Sale #{self.sale.id}, Reason: {self.reason[:30] + '...' if len(self.reason) > 33 else self.reason}"
