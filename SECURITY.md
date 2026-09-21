# Politique de sécurité

## Signaler une vulnérabilité

Ce dépôt est un projet de portfolio (tests de non-régression de sécurité applicative). Si tu identifies un problème de sécurité dans le code lui-même (gestion des identifiants de test, exécution de commandes, workflow CI), merci de :

1. Ne pas ouvrir d'issue publique décrivant le détail du problème.
2. Contacter directement l'auteure via le profil GitHub ([nblitte](https://github.com/nblitte)) ou LinkedIn.
3. Décrire le problème, les étapes de reproduction et l'impact estimé.

## Portée

- La cible des tests est **OWASP Juice Shop**, une application volontairement vulnérable, lancée **en local ou en CI éphémère uniquement**. Les vulnérabilités de Juice Shop ne sont pas dans la portée de ce dépôt.
- Les identifiants présents dans `config/env.example.json` sont les comptes de démonstration publics de Juice Shop. `config/env.json` (identifiants réels éventuels) n'est jamais versionné.
- Ces tests ne doivent être exécutés que contre des applications dont tu es propriétaire ou pour lesquelles tu disposes d'une autorisation écrite.
- Aucune fonctionnalité offensive n'est fournie : les tests **vérifient** des contrôles (authentification, RBAC, non-verbosité des erreurs), ils n'exploitent rien.
