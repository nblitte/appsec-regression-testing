from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url

    def open(self, path: str):
        self.driver.get(f"{self.base_url}{path}")

    def wait_visible(self, by: By, value: str, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    def wait_url_contains(self, fragment: str, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(fragment))

    def page_source_lower(self) -> str:
        return (self.driver.page_source or "").lower()

    def dismiss_cookie_banner_if_present(self):
        # Bandeau cookie Juice Shop : peut varier selon la version
        candidates = [
            "button[aria-label='dismiss cookie message']",
            "button[aria-label='Close Welcome Banner']",
            "button.close-dialog",
        ]
        for sel in candidates:
            try:
                btn = self.driver.find_element(By.CSS_SELECTOR, sel)
                btn.click()
                return True
            except NoSuchElementException:
                continue
        return False
