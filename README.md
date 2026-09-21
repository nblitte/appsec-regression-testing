# appsec-regression-testing

Tests de **non-régression de sécurité applicative** contre [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) : une suite Web (Selenium + Pytest) et une suite API (Postman/Newman), exécutées automatiquement en CI (GitHub Actions ou Jenkins) avec rapports HTML/JUnit publiés comme **preuves d'exécution**.

> Objectif : montrer comment transformer des contrôles de sécurité (authentification, contrôle d'accès par rôle, non-verbosité des erreurs) en tests automatisés qui alertent dès qu'un correctif régresse. Tests **défensifs** uniquement : aucune exploitation.

## Ce qui est vérifié

| Couche | Contrôle | Fichier |
|---|---|---|
| Web | Une page protégée redirige vers le login si non authentifié | `web/tests/test_auth_redirect.py` |
| Web | Un utilisateur standard n'accède pas à l'UI d'administration (RBAC) | `web/tests/test_role_based_access_ui.py` |
| Web | Après déconnexion, la session n'ouvre plus les pages protégées | `web/tests/test_logout_invalidates_session.py` |
| Web | Un login échoué ne divulgue pas de détails techniques (stack trace, SQL…) | `web/tests/test_error_messages_not_verbose.py` |
| API | Endpoint public accessible, endpoint protégé refusé sans token | `api/postman_collection.json` |
| API | RBAC : token « user » refusé (403) et token « admin » accepté (200) sur un endpoint admin | `api/postman_collection.json` |

Les tokens sont récupérés dynamiquement par `api/get_tokens.py` (login réel), puis injectés dans l'environnement Postman.

## Architecture

```
web/            Selenium + Pytest (Page Object : pages/, tests/)
api/            get_tokens.py + collection/environnement Postman + run_newman_v2.sh
config/         env.example.json (à copier en env.json) + schéma JSON de validation
scripts/        bootstrap.sh, run_all.sh, generate_summary_md.py
Jenkinsfile     Pipeline déclaratif (alternative à GitHub Actions)
.github/        ci.yml (tests + publication des rapports sur GitHub Pages), dependabot.yml
```

## Démarrage rapide

Prérequis : Python 3.11+, Node.js 20+, Chrome/Chromium, Docker.

```bash
# 1. Lancer la cible (application volontairement vulnérable, en local uniquement)
docker run -d --name juice-shop -p 3000:3000 bkimminich/juice-shop

# 2. Installer les dépendances
./scripts/bootstrap.sh
npm i -g newman newman-reporter-htmlextra

# 3. Configurer
cp config/env.example.json config/env.json

# 4. Tout exécuter (Web + API + résumé)
./scripts/run_all.sh
```

Les rapports sont écrits dans `reports/` (`pytest-report.html`, `newman-report.html`, fichiers JUnit, `SUMMARY.md`). Le script retourne un code non nul si un contrôle a régressé, tout en générant les rapports.

Variable optionnelle : `CHROME_BIN=/chemin/vers/chrome` pour utiliser un binaire Chrome/Chromium précis (le chromedriver est résolu automatiquement par Selenium Manager).

## Intégration continue

- **GitHub Actions** (`.github/workflows/ci.yml`) : démarre Juice Shop dans Docker, exécute les suites, publie le résumé JUnit, archive les rapports, puis les publie sur GitHub Pages (uniquement depuis `main`). Permissions minimales par job.
- **Jenkins** (`Jenkinsfile`) : mêmes étapes, avec `junit` et `archiveArtifacts` en post-build.
- **Dependabot** : mises à jour hebdomadaires des dépendances pip et des actions GitHub.

## Validation de ce projet

- Lint : `actionlint` (workflows) et `shellcheck` (scripts) sans avertissement.
- Suite API : validée contre un faux serveur imitant les endpoints Juice Shop, y compris un scénario de **régression volontaire** du RBAC qui fait bien échouer la collection.
- Suite Web : validée contre une petite SPA factice reproduisant les sélecteurs de Juice Shop ; 4 tests passent, et une régression RBAC volontairement introduite fait échouer le test attendu.
- Point d'attention : les sélecteurs Web peuvent varier selon la version de Juice Shop (les tests essaient plusieurs candidats). Si un sélecteur ne correspond plus, l'échec l'indique explicitement (`Update selectors`).

## Cadre d'utilisation

À n'exécuter que contre des cibles dont vous êtes propriétaire ou autorisé(e) à tester. Voir [SECURITY.md](SECURITY.md).

## Licence

[MIT](LICENSE)
