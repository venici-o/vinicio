from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Conta
@login_required
def accounts_list(request):
    return render(request, 'bank_accounts/myaccounts.html')

#tela para adicionar conta
def register_account(request):
    if request.method == "POST":
        method = request.POST.get("method")

        if method == "manual":
            return redirect("manual_account")

        elif method == "automatic":
            return redirect("automatic_account")

    return render(request, "bank_accounts/register_account.html")

def register_manual(request):
    return render(request, 'bank_accounts/register_manual.html')

def register_auto(request):
    return render(request, 'bank_accounts/register_auto.html')