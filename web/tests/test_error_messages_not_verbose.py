from web.pages.login_page import LoginPage

SENSITIVE_MARKERS = [
    "traceback",
    "exception",
    "stack trace",
    "nullpointer",
    "sql",
    "syntax error",
    "org.springframework",
    "at com.",
    "php warning",
    "fatal error",
]


def test_login_error_not_verbose(driver, base_url, env):
    login = LoginPage(driver, base_url)
    login.open(env["login_path"])
    login.dismiss_cookie_banner_if_present()

    # Mauvais mot de passe volontaire (test de non-verbosité)
    login.login(env["test_users"]["standard"]["username"], "wrong-password")

    source = (driver.page_source or "").lower()
    for marker in SENSITIVE_MARKERS:
        assert marker not in source, f"Sensitive marker leaked in UI: {marker}"
