from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon_folder = models.FilePathField(
        allow_folders=True, allow_files=False, verbose_name='Папка иконки',
        default=None, null=True, blank=True)
    icon_file = models.ImageField(verbose_name='Файл иконки', default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    start_balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Начальный баланс')
    icon_folder = models.FilePathField(
        allow_folders=True, allow_files=False, verbose_name='Папка иконки',
        default=None, null=True, blank=True)
    icon_file = models.ImageField(verbose_name='Файл иконки', default=None, null=True, blank=True)

    def __str__(self):
        return self.name


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
        verbose_name='Тип транзакции'
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

    def __str__(self):
        return self.type_transaction + ', ' + str(self.amount) + ' ' + str(self.date_added)
