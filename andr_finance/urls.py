from django.urls import path
from . import views

app_name = 'andr_finance'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/', views.accounts, name='accounts'),
    path('categories/', views.categories, name='categories'),
    path('new_category/', views.new_category, name='new_category'),
]