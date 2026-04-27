from django.test import tag
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from .base import E2EBaseTest


@tag("e2e")
class TransactionsE2ETest(E2EBaseTest):
    def setUp(self):
        self.user = self.create_user()
        self.login_via_ui()

    def _fill_transaction_form(self, tx_type, name, value):
        self.goto("transactions:create_transaction")
        Select(
            self.driver.find_element(By.CSS_SELECTOR, "select[name=transaction_type]")
        ).select_by_value(tx_type)
        name_input = self.driver.find_element(By.ID, "name-input")
        name_input.clear()
        name_input.send_keys(name)
        # Set value via JS to bypass the locale-dependent input formatter
        self.driver.execute_script(
            f"document.getElementById('value-input').value = '{value}';"
        )
        # Clear the default category_id so no invalid FK is sent
        self.driver.execute_script(
            "document.getElementById('selected-category').value = '';"
        )
        create_url = self.driver.current_url
        self.driver.find_element(By.ID, "sent-transaction-btn").click()
        # Wait for redirect away from the create page
        self.wait().until(EC.url_changes(create_url))

    def test_create_deposit_appears_in_list(self):
        """Creating a DEPOSIT transaction redirects to list and shows the entry."""
        self._fill_transaction_form("DEPOSIT", "Salário Teste", "2500.00")

        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Salário Teste", body_text)

    def test_create_withdrawal_appears_in_list(self):
        """Creating a WITHDRAWAL transaction redirects to list and shows the entry."""
        self._fill_transaction_form("WITHDRAWAL", "Conta de Luz", "180.00")

        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Conta de Luz", body_text)

    def test_missing_field_shows_validation_error(self):
        """Submitting the transaction form without a name shows a validation error."""
        self.goto("transactions:create_transaction")
        Select(
            self.driver.find_element(By.CSS_SELECTOR, "select[name=transaction_type]")
        ).select_by_value("DEPOSIT")
        # Remove the required attribute so the browser does not block submission
        self.driver.execute_script(
            "document.getElementById('name-input').removeAttribute('required');"
        )
        self.driver.execute_script(
            "document.getElementById('selected-category').value = '';"
        )
        value_input = self.driver.find_element(By.ID, "value-input")
        value_input.clear()
        value_input.send_keys("50.00")
        self.driver.find_element(By.ID, "sent-transaction-btn").click()

        self.wait().until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Informe o nome')]")
            )
        )
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Informe o nome", body_text)
