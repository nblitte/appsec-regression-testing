#!/usr/bin/env bash
# Exécute toute la chaîne. Les échecs de tests ne bloquent pas la génération
# des rapports : on mémorise le code de sortie et on l'applique à la fin,
# pour que la CI échoue (régression) tout en ayant produit les preuves.
set -uo pipefail

mkdir -p reports
status=0

# shellcheck disable=SC1091
source .venv/bin/activate

# Web tests + rapport HTML
pytest \
  --junitxml=reports/pytest-junit.xml \
  --html=reports/pytest-report.html \
  --self-contained-html || status=1

# Récupération des tokens (user/admin) pour les tests API
python api/get_tokens.py || status=1

# API tests + rapport HTML
bash api/run_newman_v2.sh || status=1

# Résumé exécutif Markdown (preuve d'exécution)
python scripts/generate_summary_md.py

if (( status )); then
  echo "❌ Au moins un contrôle de sécurité a régressé. Voir ./reports"
else
  echo "✅ Done. Reports in ./reports"
fi
exit "$status"
