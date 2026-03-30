from django.urls import path
from . import views

app_name = "budget"

urlpatterns = [
    path('', views.budget_view, name='list'),
    path('set/', views.set_budget, name='set_budget'),
]