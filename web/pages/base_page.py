from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Textes affichés par Juice Shop quand l'accès est refusé (page « 403 »).
DENIED_MARKERS = ("403", "forbidden", "not authorized", "not allowed")


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

    def visible_text_lower(self) -> str:
        """Texte réellement affiché (pas le code source, qui contient des scripts)."""
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text.lower()
        except WebDriverException:
            return ""

    def wait_access_denied(self, login_path: str, timeout: int = 10) -> bool:
        """Attend que l'accès soit refusé : redirection vers le login OU page 403.

        Selon la version de Juice Shop, une route protégée renvoie vers /#/login
        ou affiche « You are not allowed to access this page! ».
        """

        def denied(driver):
            if login_path in driver.current_url:
                return True
            text = self.visible_text_lower()
            return any(m in text for m in DENIED_MARKERS)

        try:
            WebDriverWait(self.driver, timeout).until(denied)
            return True
        except TimeoutException:
            return False

    def click_first(self, selectors, timeout: int = 8) -> bool:
        """Clique sur le premier sélecteur cliquable parmi plusieurs candidats.

        Les sélecteurs varient d'une version de Juice Shop à l'autre.
        """
        end_each = max(1, timeout // max(1, len(selectors)))
        for sel in selectors:
            try:
                el = WebDriverWait(self.driver, end_each).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                )
                el.click()
                return True
            except (TimeoutException, WebDriverException):
                continue
        return False

    def dismiss_overlays(self, timeout: int = 5):
        """Ferme la fenêtre de bienvenue et le bandeau cookies de Juice Shop.

        Les deux apparaissent avec un léger délai : on les attend brièvement.
        """
        for sel in (
            "button[aria-label='Close Welcome Banner']",
            "[aria-label='dismiss cookie message']",
        ):
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                ).click()
            except (TimeoutException, WebDriverException):
                continue
