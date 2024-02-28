from django.urls import path
from . import views

app_name = 'andr_finance'

urlpatterns = [
    path('', views.index, name='index'),

    path('categories/', views.categories, name='categories'),
    path('category_new/', views.category_new, name='category_new'),
    path('category_edit/<int:category_id>/', views.category_edit, name='category_edit'),
    path('category_delete/<int:category_id>/', views.category_delete, name='category_delete'),

    path('currencies/', views.currencies, name='currencies'),
    path('currency_new/', views.currency_new, name='currency_new'),
    path('currency_edit/<int:currency_id>/', views.currency_edit, name='currency_edit'),
    path('currency_delete/<int:currency_id>/', views.currency_delete, name='currency_delete'),

    path('accounts/', views.accounts, name='accounts'),
    path('account_new/', views.account_new, name='account_new'),
    path('account_edit/<int:account_id>/', views.account_edit, name='account_edit'),

    path('transactions/', views.transactions, name='transactions'),
    path('transaction_new/', views.transaction_new, name='transaction_new'),
    path('transaction_edit/<int:transaction_id>/', views.transaction_edit, name='transaction_edit'),
    path('transaction_delete/<int:transaction_id>/', views.transaction_delete, name='transaction_delete'),
]
