from django.db import models

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=250)
    additionalInfo = models.TextField(max_length=500)

    def __str__(self):
        return self.name

class Expense(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(max_length=500)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount}  - {self.category}"
    class Meta:
        ordering = ['-date']
