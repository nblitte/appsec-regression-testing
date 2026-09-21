# appsec-regression-testing

Tests de **non-régression de sécurité applicative** contre [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) : une suite Web (Selenium + Pytest) et une suite API (Postman/Newman), exécutées automatiquement en CI (GitHub Actions ou Jenkins) avec rapports HTML/JUnit publiés comme **preuves d'exécution**.

> Objectif : montrer comment transformer des contrôles de sécurité (authentification, contrôle d'accès par rôle, non-verbosité des erreurs) en tests automatisés qui alertent dès qu'un correctif régresse. Tests **défensifs** uniquement : aucune exploitation.

## Ce qui est vérifié

| Couche | Contrôle | Fichier |
|---|---|---|
| Web | L'UI d'administration n'est pas accessible sans authentification (redirection login ou page 403) | `web/tests/test_auth_redirect.py` |
| Web | Un utilisateur standard n'accède pas à l'UI d'administration (RBAC) | `web/tests/test_role_based_access_ui.py` |
| Web | Après déconnexion, la session n'ouvre plus les pages protégées | `web/tests/test_logout_invalidates_session.py` |
| Web | Un login échoué affiche un message d'erreur sans détail technique (stack trace, SQL…) | `web/tests/test_error_messages_not_verbose.py` |
| API | Endpoint public accessible ; `whoami` anonyme n'expose aucune identité ; `whoami` avec token renvoie bien le propriétaire | `api/postman_collection.json` |
| API | `/api/Users` refusé sans token, accepté avec un token valide | `api/postman_collection.json` |
| API | RBAC : `/rest/order-history/orders` (réservé au rôle *accounting*) refusé sans token et avec un token « utilisateur », accepté avec le compte comptable | `api/postman_collection.json` |

Le compte « standard » de test est créé automatiquement (inscription libre de Juice Shop, idempotente) : aucune dépendance à un compte de démo dont les identifiants changent selon les versions. Les tokens sont récupérés par `api/get_tokens.py` puis injectés dans l'environnement Postman.

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

- Lint : `actionlint` (workflows), `shellcheck` (scripts) et `pyflakes` sans avertissement.
- Un premier run de CI contre le vrai Juice Shop a révélé des hypothèses fausses dans la première version (comptes de démo, `whoami` anonyme qui répond 200, `/api/Challenges` public, sélecteurs et fenêtres de bienvenue). Les tests ont été corrigés à partir du comportement documenté de Juice Shop (routes protégées de `server.ts`, comptes de `users.yml`).
- Les suites Web et API sont validées contre un faux serveur reproduisant ce comportement, y compris une **régression RBAC volontaire** qui fait bien échouer la collection Newman.
- Les sélecteurs Web peuvent varier selon la version de Juice Shop (plusieurs candidats sont essayés). En cas d'échec, le message indique le sélecteur à mettre à jour.

## Cadre d'utilisation

À n'exécuter que contre des cibles dont vous êtes propriétaire ou autorisé(e) à tester. Voir [SECURITY.md](SECURITY.md).

## Licence

[MIT](LICENSE)
