from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Conta

@login_required
def accounts_list(request):
    contas = Conta.objects.all()
    return render(request, 'bank_accounts/myaccounts.html')