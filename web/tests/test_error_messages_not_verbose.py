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
    login.dismiss_overlays()

    # Mauvais mot de passe volontaire (test de non-verbosité)
    login.login(env["test_users"]["standard"]["username"], "wrong-password")

    # On attend le message d'erreur : sinon le test passerait à vide.
    message = login.wait_error_message().lower()
    assert message, "No error message displayed after a failed login."

    visible = login.visible_text_lower()
    for marker in SENSITIVE_MARKERS:
        assert marker not in visible, f"Sensitive marker leaked in UI: {marker}"
