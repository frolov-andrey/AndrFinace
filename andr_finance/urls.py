from django.urls import path
from . import views

app_name = 'andr_finance'

urlpatterns = [
    path('', views.index, name='index'),

    path('categories/', views.categories, name='categories'),
    path('new_category/', views.new_category, name='new_category'),

    path('currencies/', views.currencies, name='currencies'),
    path('new_currency/', views.new_currency, name='new_currency'),
    path('edit_currency/<int:currency_id>/', views.edit_currency, name='edit_currency'),

    path('accounts/', views.accounts, name='accounts'),
]