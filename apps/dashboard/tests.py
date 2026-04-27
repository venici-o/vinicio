from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from apps.transactions.models import Transaction
from apps.goals.models import Goal
from apps.budget.models import Budget
from .services import build_dashboard_context


def make_transaction(user, value, transaction_type, days_ago=0):
    t = Transaction.objects.create(
        user=user, name="tx", value=value, transaction_type=transaction_type
    )
    if days_ago:
        Transaction.objects.filter(pk=t.pk).update(
            date=date.today() - timedelta(days=days_ago)
        )
    return t


def make_goal(user, deadline_days=30, is_completed=False, target=Decimal("1000.00")):
    return Goal.objects.create(
        user=user,
        name="Meta",
        target_amount=target,
        deadline=date.today() + timedelta(days=deadline_days),
        is_completed=is_completed,
    )


def make_budget(user, limit):
    return Budget.objects.create(user=user, month=date.today().replace(day=1), limit=limit)


class DashboardServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")

    def test_empty_user_returns_is_empty_true(self):
        ctx = build_dashboard_context(self.user)
        self.assertTrue(ctx["is_empty"])

    def test_balance_is_deposits_minus_withdrawals(self):
        make_transaction(self.user, Decimal("500.00"), "DEPOSIT")
        make_transaction(self.user, Decimal("200.00"), "WITHDRAWAL")
        ctx = build_dashboard_context(self.user)
        self.assertEqual(ctx["total_balance"], Decimal("300.00"))

    def test_month_aggregates_only_current_month(self):
        make_transaction(self.user, Decimal("1000.00"), "DEPOSIT", days_ago=40)
        make_transaction(self.user, Decimal("100.00"), "DEPOSIT")
        ctx = build_dashboard_context(self.user)
        self.assertEqual(ctx["month_summary"]["income"], Decimal("100.00"))

    def test_nearest_goal_picks_smallest_future_deadline(self):
        make_goal(self.user, deadline_days=60)
        closer = make_goal(self.user, deadline_days=10)
        ctx = build_dashboard_context(self.user)
        self.assertEqual(ctx["priority_goal"].pk, closer.pk)

    def test_budget_level_warning_at_80_percent_boundary(self):
        make_budget(self.user, Decimal("100.00"))
        make_transaction(self.user, Decimal("80.00"), "WITHDRAWAL")
        ctx = build_dashboard_context(self.user)
        self.assertEqual(ctx["budget_status"]["level"], "warning")

    def test_budget_level_exceeded_at_100_percent_boundary(self):
        make_budget(self.user, Decimal("100.00"))
        make_transaction(self.user, Decimal("100.00"), "WITHDRAWAL")
        ctx = build_dashboard_context(self.user)
        self.assertEqual(ctx["budget_status"]["level"], "exceeded")

    def test_budget_status_none_when_no_budget_for_month(self):
        ctx = build_dashboard_context(self.user)
        self.assertIsNone(ctx["budget_status"])
