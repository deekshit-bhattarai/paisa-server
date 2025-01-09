from django.db import models
from django.contrib.auth.models import User

INCOME_AT = [("Bank", "Bank"), ("Cash", "Cash"), ("Wallet", "Wallet")]
EXPENSE_FROM = [("Bank", "Bank"), ("Cash", "Cash"), ("Wallet", "Wallet")] 

class ExpenseCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length = 20)

class IncomeTracker(models.Model):
    amount = models.DecimalField(max_digits=12, default=0, decimal_places=2)
    source = models.CharField(max_length=50, choices=INCOME_AT)
    reason = models.CharField(max_length=50)
    remarks = models.TextField()
    time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ExpenseTracker(models.Model):
    amount = models.DecimalField(max_digits=12, default=0, decimal_places=2)
    source = models.CharField(max_length=50, choices=EXPENSE_FROM)
    reason = models.CharField(max_length=50)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, null=True, blank=True)
    remarks = models.TextField()
    time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['time']
