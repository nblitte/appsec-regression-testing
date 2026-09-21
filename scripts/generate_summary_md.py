"""Génère un résumé exécutif Markdown listant les artefacts produits par le run."""

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUT = REPORTS / "SUMMARY.md"


def exists(name: str) -> str:
    return "✅" if (REPORTS / name).exists() else "❌"


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"""# Résumé d'exécution — AppSec non-régression

**Date :** {now}

## Artefacts

| Élément | Présent |
|---|---|
| Pytest HTML (`pytest-report.html`) | {exists("pytest-report.html")} |
| Pytest JUnit (`pytest-junit.xml`) | {exists("pytest-junit.xml")} |
| Newman HTML (`newman-report.html`) | {exists("newman-report.html")} |
| Newman JUnit (`newman-junit.xml`) | {exists("newman-junit.xml")} |

## Interprétation rapide

- Si un test échoue : considérer cela comme une **régression** d'un contrôle de sécurité.
- Conserver ces artefacts comme **preuves** (audit / GRC / suivi correctifs).

## Notes

- Les rapports HTML sont inclus dans le dossier `reports/` et archivés en CI (Jenkins/GitHub Actions).
"""
    OUT.write_text(content, encoding="utf-8")
    print(f"[+] Wrote {OUT}")


if __name__ == "__main__":
    main()
