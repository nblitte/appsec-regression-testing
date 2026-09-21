from web.pages.base_page import BasePage


def test_unauthenticated_cannot_access_admin_ui(driver, base_url, env):
    page = BasePage(driver, base_url)
    page.open(env["admin_path"])
    page.dismiss_overlays()
    # Selon la version : redirection vers /#/login ou page « 403 ».
    assert page.wait_access_denied(env["login_path"]), (
        f"Admin UI reachable without authentication (url: {driver.current_url})"
    )
