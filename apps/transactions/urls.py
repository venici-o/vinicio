from django.urls import path
from . import views

app_name = "transactions"

urlpatterns = [
    path("", views.get_transactions, name="list"),  # buscar as transações
    path("create/", views.create_transactions, name="create_transaction"), #criar uma nova transação
    path('post/', views.post_transaction, name="post_transaction"), # enviar uma transação
    
    #criar rota pra criar nova categoria "create_category/"
    path("create_category/", views.create_category, name="create_category"),
    path("<int:pk>/edit/", views.edit_transaction, name="update"),
    path("<int:pk>/delete/", views.delete_transaction, name="delete"),
]
