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
    name = models.CharField(max_length=200, verbose_name='Название')
    start_balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Начальный баланс')
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, verbose_name='Валюта')
    icon = models.ImageField()

    def __str__(self):
        return self.name + ', ' + self.currency.name


class Transaction(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.DO_NOTHING,
        related_name='accounts',
        verbose_name='Счет'
    )
    account_recipient = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING,
        related_name='account_recipient',
        blank=True, null=True,
        verbose_name='Счет получатель'
    )
    RECEIPT = 'receipt'
    EXPENSE = 'expense'
    TRANSFER = 'transfer'
    CHANGE_CHOICES = {
        RECEIPT: 'Доход',
        EXPENSE: 'Расход',
        TRANSFER: 'Перевод',
    }
    change = models.CharField(
        max_length=20,
        choices=CHANGE_CHOICES,
        default=RECEIPT,
        verbose_name='Тип транзакции 2'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name='Категория'
    )
    date_added = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.change + ', ' + self.amount + ' ' + str(self.date_added)
