"""
Récupère un token utilisateur standard et un token admin via l'API de login
de Juice Shop (POST /rest/user/login), et les injecte dans
api/postman_environment.json pour que les collections Postman/Newman
puissent les utiliser (variables {{user_token}} / {{admin_token}}).

Aucune exploitation : simple appel à l'endpoint de connexion documenté,
avec des comptes de test déclarés dans config/env.json.
"""

import json
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
ENV_JSON = ROOT / "config" / "env.json"
POSTMAN_ENV = ROOT / "api" / "postman_environment.json"

LOGIN_ENDPOINT = "/rest/user/login"  # Juice Shop


def load_env():
    if not ENV_JSON.exists():
        raise FileNotFoundError(f"Missing {ENV_JSON}. Create it from config/env.example.json")
    return json.loads(ENV_JSON.read_text(encoding="utf-8"))


def post_login(base_url: str, email: str, password: str) -> str:
    url = base_url.rstrip("/") + LOGIN_ENDPOINT
    resp = requests.post(url, json={"email": email, "password": password}, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    # Juice Shop renvoie généralement un token dans authentication.token
    token = None
    if isinstance(data, dict):
        token = (data.get("authentication", {}) or {}).get("token")

    if not token:
        raise RuntimeError(f"Token not found in login response: {data}")
    return token


def update_postman_env(values: dict):
    env = json.loads(POSTMAN_ENV.read_text(encoding="utf-8"))
    env_map = {v["key"]: v for v in env.get("values", [])}

    for key, value in values.items():
        if key in env_map:
            env_map[key]["value"] = value
            env_map[key]["enabled"] = True
        else:
            env.setdefault("values", []).append({"key": key, "value": value, "enabled": True})

    POSTMAN_ENV.write_text(json.dumps(env, indent=2), encoding="utf-8")


def main():
    env = load_env()
    base_url = env["api"]["base_url"]

    user_email = env["test_users"]["standard"]["username"]
    user_pass = env["test_users"]["standard"]["password"]
    admin_email = env["test_users"]["admin"]["username"]
    admin_pass = env["test_users"]["admin"]["password"]

    print("[*] Fetching user token...")
    user_token = post_login(base_url, user_email, user_pass)
    print("[*] Fetching admin token...")
    admin_token = post_login(base_url, admin_email, admin_pass)

    update_postman_env(
        {
            "user_email": user_email,
            "admin_email": admin_email,
            "user_token": user_token,
            "admin_token": admin_token,
        }
    )

    print(f"[+] Updated {POSTMAN_ENV} with user_token/admin_token.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001 — script CLI simple, on affiche et sort
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)
