# 🤝 Guide de contribution

Merci de vouloir aider à améliorer **Streamlit-app Project** !

## 🛠️ Configuration du poste de travail

Le projet utilise `uv`.

1. Cloner le dépôt :

```bash
git clone <url>
```

2. Synchroniser l'environnement :

```bash
uv sync
```

## 🧪 Cycle de validation

Avant de soumettre une Pull Request :

* **Linting :**

```bash
uv run ruff check .
```

* **Tests & Couverture :**

```bash
uv run pytest --cov=app "--cov-report=html:docs/source/_static/coverage" tests/
```

* **Documentation :**

```bash
uv run sphinx-build -b html docs/source docs/build/html
```

## 🚀 Soumission

Créez une branche `feature/nom` et ouvrez une Pull Request vers `main`.
