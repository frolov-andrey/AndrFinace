from django.urls import path
from . import views

app_name = 'andr_finance'

urlpatterns = [
    path('', views.index, name='index'),

    path('categories/', views.categories, name='categories'),
    path('new_category/', views.new_category, name='new_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),

    path('currencies/', views.currencies, name='currencies'),
    path('new_currency/', views.new_currency, name='new_currency'),
    path('edit_currency/<int:currency_id>/', views.edit_currency, name='edit_currency'),

    path('accounts/', views.accounts, name='accounts'),
    path('new_account/', views.new_account, name='new_account'),
    path('edit_account/<int:account_id>/', views.edit_account, name='edit_account'),

    path('transactions/', views.transactions, name='transactions'),
    path('new_transaction/', views.new_transaction, name='new_transaction'),
    path('edit_transaction/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('delete_transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
]
