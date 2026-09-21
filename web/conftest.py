import json
import os
from pathlib import Path

import pytest
from jsonschema import validate
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"


def load_env():
    env_path = CONFIG_DIR / "env.json"
    if not env_path.exists():
        raise FileNotFoundError(
            f"Missing {env_path}. Create it from config/env.example.json"
        )
    schema = json.loads((CONFIG_DIR / "env.schema.json").read_text(encoding="utf-8"))
    data = json.loads(env_path.read_text(encoding="utf-8"))
    validate(instance=data, schema=schema)
    return data


@pytest.fixture(scope="session")
def env():
    return load_env()


@pytest.fixture(scope="session")
def base_url(env):
    return env["base_url"].rstrip("/")


@pytest.fixture
def driver():
    opts = Options()
    # CI-friendly
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1440,900")

    # Binaire Chrome personnalisé (optionnel) : CHROME_BIN=/chemin/vers/chrome
    chrome_bin = os.environ.get("CHROME_BIN")
    if chrome_bin:
        opts.binary_location = chrome_bin

    # Selenium Manager (intégré à Selenium >= 4.6) télécharge/résout le bon
    # chromedriver automatiquement : pas besoin de webdriver-manager.
    drv = webdriver.Chrome(options=opts)
    drv.set_page_load_timeout(20)
    yield drv
    drv.quit()
