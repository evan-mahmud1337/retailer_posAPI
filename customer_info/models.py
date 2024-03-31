from django.db import models
import uuid
from inventory.models import Varient
# Create your models here.

class Customer_info(models.Model):
    name=models.CharField(max_length=50)
    number =models.IntegerField()
    address=models.CharField(max_length=200)
    date_joined = models.DateField(auto_now_add=True,null=True, verbose_name="Joined time")
    def __str__(self):
        return self.name


class Sales(models.Model):
    usersales = models.ForeignKey(Customer_info, on_delete=models.CASCADE)
    product_id=models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    product_varient=models.ForeignKey(Varient,on_delete=models.CASCADE,null=True,blank=True)
    vat=models.IntegerField()
    tax=models.IntegerField()
    discount=models.IntegerField()
    price=models.IntegerField()
    delivery_cost=models.IntegerField()
    received_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_total_price(self):
        total=self.price
        discount=self.discount
        float_total=format(total,'0.2f')
        return float_total
