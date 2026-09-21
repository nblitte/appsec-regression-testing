from web.pages.base_page import BasePage


def test_unauthenticated_redirects_to_login(driver, base_url, env):
    page = BasePage(driver, base_url)
    page.open(env["admin_path"])
    # Juice Shop renvoie généralement vers /#/login
    page.wait_url_contains(env["login_path"])
    assert env["login_path"] in driver.current_url
