"""Petit client pour l'API de Juice Shop : inscription idempotente et login."""

import requests

LOGIN_ENDPOINT = "/rest/user/login"
USERS_ENDPOINT = "/api/Users"


def ensure_user(base_url: str, email: str, password: str) -> None:
    """Crée le compte de test s'il n'existe pas (Juice Shop autorise l'inscription libre).

    Un 400 « email must be unique » signifie que le compte existe déjà : c'est OK.
    Cela évite de dépendre d'un compte de démo dont les identifiants varient
    selon les versions.
    """
    resp = requests.post(
        base_url.rstrip("/") + USERS_ENDPOINT,
        json={"email": email, "password": password, "passwordRepeat": password},
        timeout=15,
    )
    if resp.status_code in (200, 201):
        return
    if resp.status_code == 400 and "unique" in resp.text.lower():
        return
    resp.raise_for_status()


def post_login(base_url: str, email: str, password: str) -> str:
    """Retourne le token JWT (authentication.token) ou lève une erreur explicite."""
    resp = requests.post(
        base_url.rstrip("/") + LOGIN_ENDPOINT,
        json={"email": email, "password": password},
        timeout=15,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Login failed for {email!r}: HTTP {resp.status_code}")
    token = (resp.json().get("authentication") or {}).get("token")
    if not token:
        raise RuntimeError(f"Token not found in login response for {email!r}")
    return token
