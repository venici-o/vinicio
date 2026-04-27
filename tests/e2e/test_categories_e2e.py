from unittest import skip

from django.test import tag
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from apps.transactions.models import Category

from .base import E2EBaseTest


@tag("e2e")
class CategoriesE2ETest(E2EBaseTest):
    def setUp(self):
        self.user = self.create_user()
        self.login_via_ui()

    def test_create_category_appears_in_transaction_form(self):
        """A category saved in the database is selectable in the transaction form modal."""
        Category.objects.create(user=self.user, name="Lazer")

        self.goto("transactions:create_transaction")

        # The modal is rendered server-side and hidden via inline style.
        # Check its innerHTML directly — no need for JS interaction.
        modal = self.wait().until(
            EC.presence_of_element_located((By.ID, "category-modal"))
        )
        modal_html = modal.get_attribute("innerHTML")
        self.assertIn("Lazer", modal_html)

    @skip("Delete category with migration warning not yet implemented (H11 §2)")
    def test_delete_category_with_transactions_warns(self):
        """Deleting a category that has transactions should ask the user to migrate them."""

    @skip("Category summary page not yet implemented (H11 §3)")
    def test_category_summary_lists_transactions(self):
        """The category summary page lists all transactions for that category in the month."""
