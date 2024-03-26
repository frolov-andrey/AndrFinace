from django.urls import path
from . import views

app_name = 'andr_finance'

urlpatterns = [
    path('', views.index, name='index'),

    path('categories/', views.categories, name='categories'),
    path('categorys/add/', views.category_add, name='category_add'),
    path('categorys/edit/<int:category_id>/', views.category_edit, name='category_edit'),
    path('categorys/delete/<int:category_id>/', views.category_delete, name='category_delete'),

    path('accounts/', views.accounts, name='accounts'),
    path('accounts/add/', views.account_add, name='account_add'),
    path('accounts/edit/<int:account_id>/', views.account_edit, name='account_edit'),
    path('accounts/delete/<int:account_id>/', views.account_delete, name='account_delete'),

    path('transactions/', views.transactions, name='transactions'),
    path('transactions/add/<str:type_transaction>/', views.transaction_add, name='transaction_add'),
    path('transactions/edit/<str:type_transaction>/<int:transaction_id>/', views.transaction_edit, name='transaction_edit'),
    path('transactions/delete/<int:transaction_id>/', views.transaction_delete, name='transaction_delete'),

    path('reports/', views.reports, name='reports'),
]
