from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    icon_folder = models.CharField(max_length=200, default='', null=True, blank=True)
    icon_file = models.CharField(max_length=200, default='', null=True, blank=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', db_index=True)
    start_balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Начальный баланс')
    icon_folder = models.CharField(max_length=200, default='', null=True, blank=True)
    icon_file = models.CharField(max_length=200, default='', null=True, blank=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.DO_NOTHING,
        related_name='accounts',
        verbose_name='Счет',
        db_index=True
    )
    account_recipient = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING,
        related_name='account_recipient',
        blank=True, null=True,
        verbose_name='Счет получатель',
        db_index=True
    )

    MINUS = 'minus'
    PLUS = 'plus'
    TRANSFER = 'transfer'

    TYPE_TRANSACTION = {
        MINUS: 'Расход',
        PLUS: 'Доход',
        TRANSFER: 'Перевод',
    }
    type_transaction = models.CharField(
        max_length=20,
        choices=TYPE_TRANSACTION,
        default=MINUS,
        verbose_name='Тип транзакции',
        db_index=True,
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма', db_index=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Баланс', db_index=True,
                                  null=True, default=None, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name='Категория',
        db_index=True,
    )
    date_add = models.DateTimeField(db_index=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.type_transaction + ', ' + str(self.amount) + ' ' + str(self.date_add)
