# Projet Micro-services, Sécurité et Livraison Continue

## Description

Ce dépôt présente un **exemple d'architecture applicative
conteneurisée** mettant en œuvre plusieurs bonnes pratiques modernes de
développement logiciel :

-   architecture **micro-services**
-   orchestration avec **Docker Compose**
-   gestion sécurisée des **variables d'environnement**
-   **tests automatisés**
-   pipelines **CI/CD**
-   distribution des images via **registry Docker**

L'objectif est de démontrer une organisation claire d'un projet complet
allant du développement local jusqu'au déploiement automatisé.

------------------------------------------------------------------------

# Objectifs du projet

  Domaine         Objectif
  --------------- -------------------------------------------------
  Architecture    structurer une application multi-services
  Orchestration   exécuter plusieurs conteneurs interconnectés
  Persistance     stocker les données dans une base dédiée
  Sécurité        isoler les secrets du code
  Qualité         automatiser les tests
  Livraison       automatiser le build et la publication d'images

------------------------------------------------------------------------

# Architecture générale

L'application suit une architecture classique en **trois couches** :

Frontend → Backend API → Database

-   **Frontend** : interface utilisateur
-   **Backend API** : logique métier et accès aux données
-   **Database** : stockage persistant

``` mermaid
graph TD

User((Utilisateur))

subgraph Infrastructure Docker

subgraph Frontend
Front[Application Frontend]
end

subgraph Backend
API[Service API]
end

subgraph Database
DB[(Base de données)]
end

Vol[(Volume de stockage)]

end

User --> Front
Front --> API
API --> DB
DB -.-> Vol
```

------------------------------------------------------------------------

# Organisation du projet

Structure typique du dépôt :

    .
    ├── .github/
    │   └── workflows/
    │       ├── ci.yml
    │       └── cd.yml
    ├── app_front/
    │   ├── main.py
    │   ├── pages/
    │   ├── pyproject.toml
    │   └── Dockerfile
    ├── app_api/
    │   ├── main.py
    │   ├── modules/
    │   ├── models/
    │   ├── pyproject.toml
    │   └── Dockerfile
    ├── tests/
    │   ├── test_api.py
    │   └── test_modules.py
    ├── docker-compose.yml
    ├── docker-compose.prod.yml
    ├── .env.example
    ├── .gitignore
    └── .dockerignore

------------------------------------------------------------------------

# Développement local

Le projet peut être développé et testé localement avant la
conteneurisation.

## Base de données de test

Une base légère (ex : SQLite) peut être utilisée pour les phases de
développement et de tests.

⚠️ Les fichiers de base de données locaux ne doivent pas être
versionnés.

## Tests

Les tests automatisés permettent de vérifier :

-   la logique métier
-   le fonctionnement de l'API

Configuration exemple :

``` toml
[tool.pytest.ini_options]
pythonpath = ["."
testpaths = ["tests"]
```

Exécution :

``` bash
pytest
```

------------------------------------------------------------------------

# Gestion des variables d'environnement

Les informations sensibles (mots de passe, URLs, tokens) ne doivent pas
apparaître dans le code.

Fichiers recommandés :

  Fichier           Rôle
  ----------------- --------------------------------------------
  `.env`            variables locales
  `.env.example`    modèle de configuration
  `.gitignore`      exclusion des secrets
  `.dockerignore`   exclusion des fichiers inutiles des images

Exemple :

    DATABASE_URL=
    DATABASE_USER=
    DATABASE_PASSWORD=
    API_URL=

------------------------------------------------------------------------

# Orchestration avec Docker Compose

L'application peut être exécutée via Docker Compose pour démarrer tous
les services simultanément.

Exemple simplifié :

``` yaml
services:
  frontend:
    build: ./app_front
    ports:
      - "8501:8501"
  api:
    build: ./app_api
  database:
    image: postgres
```

## Persistance des données

La base de données utilise un **volume Docker** afin que les données
restent disponibles même après l'arrêt des conteneurs.

    volumes:
      database_data:

------------------------------------------------------------------------

# Intégration Continue (CI)

La pipeline CI vérifie automatiquement :

-   le format du code
-   les tests
-   la sécurité

Outils typiques : pytest, linters, scanners de secrets

------------------------------------------------------------------------

# Sécurité

Un scanner de secrets peut être intégré afin de détecter :

-   clés API
-   tokens
-   mots de passe exposés

Cela empêche leur présence dans l'historique Git.

------------------------------------------------------------------------

# Livraison Continue (CD)

Une pipeline CD permet de :

1.  construire les images Docker
2.  les taguer
3.  les publier dans un registre

Exemple de tags :

  Tag           Signification
  ------------- ---------------------------------
  latest        version courante
  commit hash   version liée à un commit précis

------------------------------------------------------------------------

# Déploiement

Le déploiement peut être réalisé via un fichier `docker-compose`
utilisant directement les images publiées.

``` yaml
services:
  api:
    image: organisation/api:latest
  frontend:
    image: organisation/frontend:latest
  database:
    image: postgres:latest
```

------------------------------------------------------------------------

# Fonctionnalités démontrées

-   architecture micro-services
-   séparation frontend / backend
-   persistance des données
-   conteneurisation Docker
-   orchestration Docker Compose
-   pipelines CI/CD
-   gestion sécurisée des secrets
-   tests automatisés

------------------------------------------------------------------------

# Utilisation

## Lancer l'application

``` bash
docker compose up
```

## Lancer les tests

``` bash
pytest
```

------------------------------------------------------------------------

# Objectif pédagogique

Ce projet sert de **base de démonstration** pour comprendre :

-   la structuration d'une application moderne
-   l'intégration de la conteneurisation dans le cycle de développement
-   les principes d'automatisation des pipelines logiciels
