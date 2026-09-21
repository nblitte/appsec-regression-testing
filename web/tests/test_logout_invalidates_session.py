from selenium.webdriver.common.by import By

from web.pages.base_page import BasePage
from web.pages.login_page import LoginPage


def test_logout_invalidates_session(driver, base_url, env):
    page = BasePage(driver, base_url)

    login = LoginPage(driver, base_url)
    login.open(env["login_path"])
    page.dismiss_cookie_banner_if_present()
    login.login_and_wait(env["test_users"]["standard"]["username"], env["test_users"]["standard"]["password"])

    # Ouvrir le menu compte (bouton compte dans la toolbar) — plusieurs
    # sélecteurs candidats car ils varient selon la version de Juice Shop.
    account_candidates = [
        "button[aria-label='Account']",
        "button[aria-label='Show/hide account menu']",
        "button#navbarAccount",
    ]
    opened = False
    for sel in account_candidates:
        try:
            driver.find_element(By.CSS_SELECTOR, sel).click()
            opened = True
            break
        except Exception:
            continue
    assert opened, "Account menu button not found. Update selectors."

    logout_candidates = [
        "button[aria-label='Logout']",
        "button#logoutButton",
        "a[aria-label='Logout']",
    ]
    clicked = False
    for sel in logout_candidates:
        try:
            driver.find_element(By.CSS_SELECTOR, sel).click()
            clicked = True
            break
        except Exception:
            continue
    assert clicked, "Logout control not found. Update selectors."

    # Vérifie qu'on ne peut plus accéder à une page protégée (admin)
    page.open(env["admin_path"])
    page.wait_url_contains(env["login_path"])
    assert env["login_path"] in driver.current_url
