#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Python deps installed."

if ! command -v newman >/dev/null 2>&1; then
  echo "⚠️  Newman not found. Install it with: npm i -g newman newman-reporter-htmlextra"
fi

if [[ ! -f config/env.json ]]; then
  echo "ℹ️  Create config/env.json from config/env.example.json:"
  echo "    cp config/env.example.json config/env.json"
fi
