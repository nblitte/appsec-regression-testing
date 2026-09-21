from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


class LoginPage(BasePage):
    # Juice Shop (Angular) — sélecteurs fiables
    EMAIL = (By.CSS_SELECTOR, "input#email")
    PASSWORD = (By.CSS_SELECTOR, "input#password")
    SUBMIT = (By.CSS_SELECTOR, "button#loginButton")

    def login(self, username: str, password: str):
        u = self.wait_visible(*self.EMAIL)
        p = self.wait_visible(*self.PASSWORD)
        u.clear()
        u.send_keys(username)
        p.clear()
        p.send_keys(password)
        self.driver.find_element(*self.SUBMIT).click()

    def login_and_wait(self, username: str, password: str, timeout: int = 10):
        """Se connecte et attend que la SPA ait quitté la page de login."""
        self.login(username, password)
        WebDriverWait(self.driver, timeout).until(
            lambda d: "/login" not in d.current_url
        )
