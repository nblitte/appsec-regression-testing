from selenium.webdriver.common.by import By

from .base_page import BasePage


class DashboardPage(BasePage):
    SIGNATURE = (By.CSS_SELECTOR, "[data-testid='dashboard'], .dashboard, main")

    def assert_loaded(self):
        self.wait_visible(*self.SIGNATURE, timeout=12)
