from django.contrib import admin

from .models import Category, Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_balance', 'icon_folder', 'icon_file')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_folder', 'icon_file')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'account_recipient', 'type_transaction', 'amount', 'date_add', 'title')
