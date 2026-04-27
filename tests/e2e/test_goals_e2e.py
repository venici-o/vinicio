from datetime import date, timedelta

from django.test import tag
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from apps.goals.models import Goal

from .base import E2EBaseTest


@tag("e2e")
class GoalsE2ETest(E2EBaseTest):
    def setUp(self):
        self.user = self.create_user()
        self.login_via_ui()
        self.future_deadline = (date.today() + timedelta(days=180)).strftime("%Y-%m-%d")

    def _create_goal_via_ui(self, name, target, deadline):
        self.goto("goals:create")
        self.driver.find_element(By.ID, "id_name").send_keys(name)
        self.driver.find_element(By.ID, "id_target_amount").send_keys(str(target))
        # Set date via JS — send_keys on type="date" is locale-dependent in Chrome
        self.driver.execute_script(
            f"document.getElementById('id_deadline').value = '{deadline}'"
        )
        create_url = self.driver.current_url
        self.driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
        self.wait().until(EC.url_changes(create_url))

    def test_create_goal_shows_zero_progress(self):
        """A newly created goal appears in the list with 0 % progress."""
        self._create_goal_via_ui("Viagem Europa", 5000, self.future_deadline)

        self.goto("goals:list")
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Viagem Europa", body_text)
        self.assertIn("0%", body_text)

    def test_contribution_updates_progress(self):
        """Contributing to a goal updates its progress percentage."""
        self._create_goal_via_ui("Fundo Emergência", 1000, self.future_deadline)

        goal = Goal.objects.get(user=self.user, name="Fundo Emergência")
        contribute_url = (
            self.live_server_url + reverse("goals:contribute", kwargs={"pk": goal.pk})
        )
        self.driver.get(contribute_url)
        self.driver.find_element(By.ID, "id_amount").send_keys("250")
        self.driver.execute_script(
            f"document.getElementById('id_date').value = '{date.today().strftime('%Y-%m-%d')}'"
        )
        contribute_current_url = self.driver.current_url
        self.driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
        self.wait().until(EC.url_changes(contribute_current_url))

        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("25", body_text)  # 250/1000 = 25 %

    def test_goal_completed_when_target_reached(self):
        """Contributing the full target amount marks the goal as completed."""
        self._create_goal_via_ui("Notebook Novo", 2000, self.future_deadline)

        goal = Goal.objects.get(user=self.user, name="Notebook Novo")
        contribute_url = (
            self.live_server_url + reverse("goals:contribute", kwargs={"pk": goal.pk})
        )
        self.driver.get(contribute_url)
        self.driver.find_element(By.ID, "id_amount").send_keys("2000")
        self.driver.execute_script(
            f"document.getElementById('id_date').value = '{date.today().strftime('%Y-%m-%d')}'"
        )
        complete_url = self.driver.current_url
        self.driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
        self.wait().until(EC.url_changes(complete_url))
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("100", body_text)

        # Verify the goal list page shows it as completed
        self.goto("goals:list")
        completed_cards = self.driver.find_elements(
            By.CSS_SELECTOR, ".goal-card--completed"
        )
        self.assertGreater(len(completed_cards), 0)
