from django.urls import path

from . import views_transaction
from . import views_category
from . import views_account
from . import views

app_name = 'andr_finance'

urlpatterns = [
    path('', views.Home.as_view(), name='index'),

    path('categories/', views_category.CategoryView.as_view(), name='categories'),
    path('categorys/add/', views_category.CategoryAdd.as_view(), name='category_add'),
    path('categorys/edit/<int:pk>/', views_category.CategoryUpdate.as_view(), name='category_edit'),
    path('categorys/delete/<int:pk>/', views_category.CategoryDelete.as_view(), name='category_delete'),

    path('accounts/', views_account.AccountView.as_view(), name='accounts'),
    path('accounts/add/', views_account.AccountAdd.as_view(), name='account_add'),
    path('accounts/edit/<int:pk>/', views_account.AccountUpdate.as_view(), name='account_edit'),
    path('accounts/delete/<int:pk>/', views_account.AccountDelete.as_view(), name='account_delete'),

    path('transactions/', views_transaction.TransactionView.as_view(), name='transactions'),

    # path('transactions/add/<str:type_transaction>/', views_transaction.transaction_add, name='transaction_add'),
    path('transactions/add/plus/', views_transaction.TransactionAddPlus.as_view(), name='transaction_add_plus'),
    path('transactions/add/minus/', views_transaction.TransactionAddMinus.as_view(), name='transaction_add_minus'),
    path('transactions/add/transfer/', views_transaction.TransactionAddTransfer.as_view(),
         name='transaction_add_transfer'),

    path('transactions/edit/plus/<int:pk>/',
         views_transaction.TransactionUpdatePlus.as_view(),
         name='transaction_edit_plus'),
    path('transactions/edit/minus/<int:pk>/',
         views_transaction.TransactionUpdateMinus.as_view(),
         name='transaction_edit_minus'),
    path('transactions/edit/transfer/<int:pk>/',
         views_transaction.TransactionUpdateTransfer.as_view(),
         name='transaction_edit_transfer'),

    path('transactions/delete/<int:pk>/', views_transaction.TransactionDelete.as_view(), name='transaction_delete'),

    path('reports/', views.reports, name='reports'),
    path('settings/', views.my_settings, name='my_settings'),
]
