from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts_list, name = 'my_accounts'),
]