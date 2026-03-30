from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_view, name='budget'),
    path('set/', views.set_budget, name='set_budget'),
]