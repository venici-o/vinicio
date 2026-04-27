from datetime import date

from django.test import tag
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from apps.transactions.models import Transaction

from .base import E2EBaseTest


@tag("e2e")
class BudgetE2ETest(E2EBaseTest):
    def setUp(self):
        self.user = self.create_user()
        self.login_via_ui()

    def _set_budget_via_ui(self, limit_value):
        self.goto("budget:set_budget")
        limit_input = self.driver.find_element(By.ID, "limit")
        limit_input.clear()
        limit_input.send_keys(str(limit_value))
        set_url = self.driver.current_url
        self.driver.find_element(By.CSS_SELECTOR, ".button-glass--primary").click()
        # Wait until we leave the set_budget page (redirected to list)
        self.wait().until(EC.url_changes(set_url))

    def _create_withdrawal(self, amount):
        Transaction.objects.create(
            user=self.user,
            name="Gasto teste",
            value=amount,
            transaction_type="WITHDRAWAL",
            date=date.today(),
        )

    def test_define_limit_and_see_percentage(self):
        """Setting a budget limit displays the percentage on the budget page."""
        self._create_withdrawal(200)
        self._set_budget_via_ui(1000)

        self.goto("budget:list")
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("1000", body_text)
        self.assertIn("%", body_text)

    def test_alert_yellow_at_80_percent(self):
        """80 %+ spending shows the warning (yellow) state on the budget page."""
        self._set_budget_via_ui(1000)
        self._create_withdrawal(850)  # 85 % of 1000

        self.goto("budget:list")
        self.wait().until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".budget-progress__bar-fill"))
        )
        bar = self.driver.find_element(By.CSS_SELECTOR, ".budget-progress__bar-fill")
        classes = bar.get_attribute("class")
        self.assertIn("bg-warning", classes)

    def test_alert_red_when_exceeded(self):
        """100 %+ spending shows the danger (red) state on the budget page."""
        self._set_budget_via_ui(500)
        self._create_withdrawal(600)  # 120 % of 500

        self.goto("budget:list")
        self.wait().until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".budget-progress__bar-fill"))
        )
        bar = self.driver.find_element(By.CSS_SELECTOR, ".budget-progress__bar-fill")
        classes = bar.get_attribute("class")
        self.assertIn("bg-danger", classes)
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("ultrapassado", body_text.lower())
