from web.pages.base_page import BasePage
from web.pages.login_page import LoginPage

# Plusieurs sélecteurs candidats : ils varient selon la version de Juice Shop.
ACCOUNT_MENU = [
    "button#navbarAccount",
    "button[aria-label='Show/hide account menu']",
    "button[aria-label='Account']",
]
LOGOUT = [
    "button#navbarLogoutButton",
    "button[aria-label='Logout']",
    "button#logoutButton",
    "a[aria-label='Logout']",
]


def test_logout_invalidates_session(driver, base_url, env):
    user = env["test_users"]["standard"]

    login = LoginPage(driver, base_url)
    login.open(env["login_path"])
    login.dismiss_overlays()
    login.login_and_wait(user["username"], user["password"])

    page = BasePage(driver, base_url)
    page.dismiss_overlays(timeout=2)
    assert page.click_first(ACCOUNT_MENU), "Account menu button not found. Update selectors."
    assert page.click_first(LOGOUT), "Logout control not found. Update selectors."

    # Après déconnexion, l'interface d'administration doit rester inaccessible.
    page.open(env["admin_path"])
    assert page.wait_access_denied(env["login_path"]), (
        f"Protected page still reachable after logout (url: {driver.current_url})"
    )
