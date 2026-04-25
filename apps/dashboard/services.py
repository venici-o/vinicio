from decimal import Decimal
from datetime import date

from django.db.models import Q, Sum
from django.db.models.functions import Coalesce


today = date.today()


def build_dashboard_context(user) -> dict:
    transactions = user.transaction_set.all()

    total_balance = transactions.aggregate(
        total=Coalesce(Sum("value", filter=Q(transaction_type="DEPOSIT")), Decimal("0.00"))
        - Coalesce(Sum("value", filter=Q(transaction_type="WITHDRAWAL")), Decimal("0.00"))
    )["total"]

    month_income = transactions.filter(
        transaction_type="DEPOSIT",
        date__year=today.year,
        date__month=today.month,
    ).aggregate(total=Coalesce(Sum("value"), Decimal("0.00")))["total"]

    month_expenses = transactions.filter(
        transaction_type="WITHDRAWAL",
        date__year=today.year,
        date__month=today.month,
    ).aggregate(total=Coalesce(Sum("value"), Decimal("0.00")))["total"]

    nearest_goal = (
        user.goals.filter(is_completed=False, deadline__gte=today)
        .order_by("deadline")
        .first()
        or user.goals.filter(is_completed=False).order_by("-created_at").first()
    )

    budget = user.budget_set.filter(
        month__year=today.year,
        month__month=today.month,
    ).first()

    if budget:
        spent = month_expenses
        percent = (spent / budget.limit * 100) if budget.limit else Decimal("0.00")
        if percent >= 100:
            level = "exceeded"
        elif percent >= 80:
            level = "warning"
        else:
            level = "ok"
        budget_status = {
            "limit": budget.limit,
            "spent": spent,
            "percent": round(percent, 1),
            "level": level,
        }
    else:
        budget_status = None

    is_empty = (
        not transactions.exists()
        and not user.goals.exists()
        and budget_status is None
    )

    return {
        "total_balance": total_balance,
        "month_income": month_income,
        "month_expenses": month_expenses,
        "nearest_goal": nearest_goal,
        "budget_status": budget_status,
        "is_empty": is_empty,
    }
