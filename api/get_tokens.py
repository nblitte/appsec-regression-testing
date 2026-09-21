"""
Prépare les jetons d'authentification pour la collection Postman/Newman :
  1. crée (si besoin) un utilisateur « standard » de test via l'API d'inscription ;
  2. se connecte avec ce compte et avec le compte « accounting » de démonstration
     de Juice Shop (POST /rest/user/login) ;
  3. écrit les tokens dans api/postman_environment.json
     (variables {{user_token}} / {{accounting_token}}).

Aucune exploitation : uniquement des endpoints documentés, avec des comptes
de test déclarés dans config/env.json.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from api.juice_api import ensure_user, post_login  # noqa: E402

ENV_JSON = ROOT / "config" / "env.json"
POSTMAN_ENV = ROOT / "api" / "postman_environment.json"


def load_env():
    if not ENV_JSON.exists():
        raise FileNotFoundError(f"Missing {ENV_JSON}. Create it from config/env.example.json")
    return json.loads(ENV_JSON.read_text(encoding="utf-8"))


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
    std = env["test_users"]["standard"]
    acc = env["test_users"]["accounting"]

    print("[*] Ensuring standard test user exists...", flush=True)
    ensure_user(base_url, std["username"], std["password"])
    print("[*] Fetching standard user token...", flush=True)
    user_token = post_login(base_url, std["username"], std["password"])
    print("[*] Fetching accounting user token...", flush=True)
    accounting_token = post_login(base_url, acc["username"], acc["password"])

    update_postman_env(
        {
            "base_url": base_url,
            "user_email": std["username"],
            "user_token": user_token,
            "accounting_token": accounting_token,
        }
    )
    print(f"[+] Updated {POSTMAN_ENV} with user_token/accounting_token.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001 — script CLI simple, on affiche et sort
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)
