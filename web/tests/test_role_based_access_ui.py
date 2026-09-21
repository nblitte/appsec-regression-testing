from web.pages.base_page import BasePage
from web.pages.login_page import LoginPage


def test_standard_user_cannot_access_admin_ui(driver, base_url, env):
    login = LoginPage(driver, base_url)
    login.open(env["login_path"])
    login.dismiss_cookie_banner_if_present()
    login.login_and_wait(env["test_users"]["standard"]["username"], env["test_users"]["standard"]["password"])

    page = BasePage(driver, base_url)
    page.open(env["admin_path"])

    # attendu : redirection login ou page interdite
    src = page.page_source_lower()
    assert (
        (env["login_path"] in driver.current_url)
        or ("403" in src)
        or ("forbidden" in src)
        or ("not authorized" in src)
    ), "Admin UI seems accessible. Update assertion if Juice Shop behavior differs."
