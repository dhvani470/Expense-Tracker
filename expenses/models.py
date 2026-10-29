from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Expense(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Card', 'Card'),
        ('Bank Transfer', 'Bank Transfer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    date = models.DateField()
    description = models.CharField(max_length=255)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    def __str__(self):
        return f"{self.category} - ₹{self.amount}"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount}"