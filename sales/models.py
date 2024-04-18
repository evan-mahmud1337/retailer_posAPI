from django.db import models
import uuid
from inventory.models import InventoryItem


class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    courierInvoice = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    id = models.CharField(primary_key=True, max_length=200, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    sale_return = models.BooleanField(default=False, blank=True, null=True)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Sale #{self.id} - {self.customer.name}"
    def save(self, *args, **kwargs):
        if not self.id:
            last_sale = Sale.objects.order_by('-id').first()
            if last_sale:
                last_invoice_number = int(last_sale.id.split('-')[1])
            else:
                last_invoice_number = 999
            new_invoice_number = last_invoice_number + 1
            self.id = f'Ara-{new_invoice_number}'
        super().save(*args, **kwargs)


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
    return_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"Return for Sale #{self.sale.id}, Reason: {self.reason[:30] + '...' if len(self.reason) > 33 else self.reason}"
