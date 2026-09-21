#!/usr/bin/env bash
# Exécute la collection Postman V2 (avec tokens + RBAC) via Newman.
# Nécessite : npm i -g newman newman-reporter-htmlextra
set -euo pipefail

mkdir -p reports

COLLECTION="api/postman_collection.json"
ENV="api/postman_environment.json"

newman run "$COLLECTION" -e "$ENV" \
  --reporters cli,junit,htmlextra \
  --reporter-junit-export "reports/newman-junit.xml" \
  --reporter-htmlextra-export "reports/newman-report.html" \
  --reporter-htmlextra-title "Juice Shop API Security Regression" \
  --reporter-htmlextra-darkTheme true
