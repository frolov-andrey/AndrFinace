from django.utils import timezone
from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    icon = models.ImageField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=200)
    start_balance = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    icon = models.ImageField()

    def __str__(self):
        return self.name + ', ' + self.currency.name


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name='accounts')
    account_recipient = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name='account_recipient', blank=True, null=True)
    RECEIPT = 'receipt'
    EXPENSE = 'expense'
    TRANSFER = 'transfer'
    CHANGE_CHOICES = {
        RECEIPT: 'receipt',
        EXPENSE: 'expense',
        TRANSFER: 'transfer',
    }
    change = models.CharField(max_length=20, choices=CHANGE_CHOICES, default=RECEIPT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.change + ', ' + self.amount + ' ' + str(self.date_added)
