from web.pages.base_page import BasePage
from web.pages.login_page import LoginPage


def test_standard_user_cannot_access_admin_ui(driver, base_url, env):
    user = env["test_users"]["standard"]

    login = LoginPage(driver, base_url)
    login.open(env["login_path"])
    login.dismiss_overlays()
    login.login_and_wait(user["username"], user["password"])

    page = BasePage(driver, base_url)
    page.open(env["admin_path"])

    assert page.wait_access_denied(env["login_path"]), (
        f"Admin UI seems accessible to a standard user (url: {driver.current_url})"
    )
