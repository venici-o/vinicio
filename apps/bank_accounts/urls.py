from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts_list, name='bank_accounts'),
    path('register/', views.register_account, name='register_account'),
    path('register/manual/', views.register_manual, name='register_manual'),
    path('register/auto/', views.register_auto, name='register_auto'),
]

#urls: .../my_accounts/
#.../my_accounts/register/