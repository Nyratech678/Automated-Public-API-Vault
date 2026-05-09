# Automated Public API Vault

Automated Public API Vault est un catalogue vivant d'API publiques. Le projet découvre des dépôts sur GitHub, les classe automatiquement par domaine, génère la documentation associée et alimente une vitrine web statique pensée pour la consultation rapide.

## Pourquoi ce projet existe

Le dépôt transforme une veille manuelle en pipeline automatisé. L'objectif est simple: identifier des API pertinentes, les organiser proprement, et offrir une interface lisible pour explorer rapidement le catalogue sans parcourir des centaines de dépôts à la main.

## Ce que tu obtiens

- Une découverte automatisée des dépôts liés aux APIs.
- Une catégorisation hybride basée sur les `topics` GitHub et un mapping lexical extensible.
- Une documentation Markdown générée par catégorie.
- Des exports JSON consommés par la vitrine web.
- Une interface front statique avec recherche instantanée, statistiques et navigation latérale.
- Un workflow GitHub Actions planifié pour maintenir le catalogue à jour.

## Architecture

1. `src/discover.py` interroge l'API GitHub et récupère les dépôts.
2. `src/filter.py` sépare les projets actifs des projets archivés ou trop anciens.
3. `src/categorizer.py` applique la logique de classification.
4. `src/writer.py` génère les README de catégorie et exporte `apis.json` et `categories.json`.
5. `cyber_vault.html` lit ces fichiers pour afficher la vitrine.

## Structure du dépôt

- `src/main.py`: point d'entrée CLI.
- `src/discover.py`: collecte des dépôts GitHub.
- `src/filter.py`: filtrage des APIs actives/inactives.
- `src/categorizer.py`: moteur de catégorisation.
- `src/writer.py`: génération de la documentation et des exports.
- `templates/`: templates Jinja2 utilisés pour les README.
- `category_mapping.json`: dictionnaire de mots-clés par catégorie.
- `cyber_vault.html`: vitrine web statique.

## Démarrage rapide

### Prérequis

- Python 3.12 ou 3.13.
- Un token GitHub dans `GITHUB_TOKEN` est recommandé pour éviter les limites de taux de l'API.

### Installation

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Générer le catalogue

```bash
python src/main.py --query "topic:api" --max-results 100
```

Le script génère:

- `README.md` à la racine;
- `categories/<categorie>/README.md`;
- `apis.json`;
- `categories.json`.

### Ouvrir la vitrine

Ouvre `cyber_vault.html` dans un navigateur depuis la racine du dépôt. La page charge automatiquement `apis.json` et `categories.json` pour afficher le catalogue.

## Personnalisation

### Mapping de catégories

Le fichier `category_mapping.json` contient les mots-clés utilisés pour la classification. C'est le bon endroit si tu veux affiner les catégories existantes ou en ajouter de nouvelles.

### Variables d'environnement

- `GITHUB_TOKEN`: améliore la limite de requêtes sur l'API GitHub.

## Automatisation

Le workflow `.github/workflows/auto-update.yml` est prévu pour:

- s'exécuter automatiquement toutes les 6 heures;
- être lancé manuellement si besoin;
- installer les dépendances;
- lancer le lint et la vérification de types;
- exécuter la curation;
- pousser les README, la vitrine et les JSON générés.

## Vérification locale

Pour un contrôle rapide avant publication:

```bash
python src/main.py --max-results 10
```

Ensuite, vérifie que la vitrine affiche bien les résultats et que les catégories générées correspondent au contenu collecté.

## Déploiement

Le dépôt est prêt pour un déploiement fondé sur les fichiers générés dans le repository. Le contenu documentaire et la vitrine statique sont produits automatiquement et peuvent être servis tels quels.

## Licence

Projet de curation d'APIs publiques. Ajoute une licence explicite si tu veux le publier sous une licence ouverte.