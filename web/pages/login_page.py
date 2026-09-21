from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


class LoginPage(BasePage):
    # Juice Shop (Angular)
    EMAIL = (By.CSS_SELECTOR, "input#email")
    PASSWORD = (By.CSS_SELECTOR, "input#password")
    SUBMIT = (By.CSS_SELECTOR, "button#loginButton")
    ERROR = (By.CSS_SELECTOR, ".error")

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
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: "/login" not in d.current_url
            )
        except TimeoutException as exc:
            raise AssertionError(
                f"Login did not complete for {username!r} (still on {self.driver.current_url}). "
                "Check the test credentials and the login selectors."
            ) from exc

    def wait_error_message(self, timeout: int = 8) -> str:
        return self.wait_visible(*self.ERROR, timeout=timeout).text
