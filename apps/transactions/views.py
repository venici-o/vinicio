from decimal import Decimal, InvalidOperation

from django.shortcuts import redirect, render
from .models import Transaction
from django.db.models import Sum, Q


def _build_create_transaction_context(form_data=None, errors=None):
    totais = Transaction.objects.aggregate(
        e=Sum('value', filter=Q(transaction_type='DEPOSIT')),
        s=Sum('value', filter=Q(transaction_type='WITHDRAWAL'))
    )
    account_balance = (totais['e'] or 0) - (totais['s'] or 0)
    return {
        'form_data': form_data or {},
        'errors': errors or {},
        'account_balance': account_balance,
        'transaction_type_choices': Transaction.TYPE_CHOICES,
    }

# exibir o formulário para criar uma nova transação
def create_transactions(request):
    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name', '').strip(),
            'transaction_type': request.POST.get('transaction_type', '').strip(),
            'value': request.POST.get('value', '').strip(),
        }
        errors = {}

        if not form_data['name']:
            errors['name'] = 'Informe o nome da transação.'
        elif len(form_data['name']) > 150:
            errors['name'] = 'O nome deve ter no máximo 150 caracteres.'

        allowed_types = {choice[0] for choice in Transaction.TYPE_CHOICES}
        if form_data['transaction_type'] not in allowed_types:
            errors['transaction_type'] = 'Selecione um tipo de transação válido.'

        raw_value = form_data['value'].replace(',', '.')
        try:
            parsed_value = Decimal(raw_value)
            if parsed_value <= 0:
                errors['value'] = 'O valor deve ser maior que zero.'
        except (InvalidOperation, ValueError):
            parsed_value = None
            errors['value'] = 'Informe um valor numérico válido.'

        if not errors:
            Transaction.objects.create(
                name=form_data['name'],
                transaction_type=form_data['transaction_type'],
                value=parsed_value,
            )
            return redirect('transactions:get_transactions')

        context = _build_create_transaction_context(form_data=form_data, errors=errors)
        return render(request, 'transactions/create_transaction.html', context)

    context = _build_create_transaction_context()
    return render(request, 'transactions/create_transaction.html', context)

# verificar e enviar os dados do form da transação para o banco de dados (ainda não implementado)
def post_transaction(request):
    return create_transactions(request)

# EXIBIR o extrato (entradas e saída) + o saldo 
def get_transactions(request):
    transactions = Transaction.objects.all().order_by('-date')
    # Cálculo do saldo total
    totais = transactions.aggregate(
        e=Sum('value', filter=Q(transaction_type='DEPOSIT')), 
        #soma das entrada 
        s=Sum('value', filter=Q(transaction_type='WITHDRAWAL')) 
    )  
    total_entradas = totais['e'] or 0
    total_saidas = totais['s'] or 0
    saldo = total_entradas - total_saidas
    #saldo = (totais['e'] or 0) - (totais['s'] or 0)
    return render(request, 'transactions/list_transactions.html', {
        'transactions': transactions, 
        'total_entradas': total_entradas, 
        'total_saidas': total_saidas,     
        'saldo': saldo                    
    })