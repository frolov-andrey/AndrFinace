from django.urls import path
from . import views

app_name = 'andr_finance'

urlpatterns = [
    path('', views.index, name='index'),

    path('categories/', views.categories, name='categories'),
    path('category_add/', views.category_add, name='category_add'),
    path('category_edit/<int:category_id>/', views.category_edit, name='category_edit'),
    path('category_delete/<int:category_id>/', views.category_delete, name='category_delete'),

    path('accounts/', views.accounts, name='accounts'),
    path('account_add/', views.account_add, name='account_add'),
    path('account_edit/<int:account_id>/', views.account_edit, name='account_edit'),
    path('account_delete/<int:account_id>/', views.account_delete, name='account_delete'),

    path('transactions/', views.transactions, name='transactions'),
    path('transaction_add/', views.transaction_add, name='transaction_add'),
    path('transaction_edit/<int:transaction_id>/', views.transaction_edit, name='transaction_edit'),
    path('transaction_delete/<int:transaction_id>/', views.transaction_delete, name='transaction_delete'),
]
