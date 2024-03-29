from django.contrib import admin

from .models import Category, Account, Transaction

admin.site.register(Category)
admin.site.register(Account)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'account_recipient', 'type_transaction', 'amount', 'date_add', 'title')
