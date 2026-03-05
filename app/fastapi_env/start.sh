#!/bin/bash

# On s'assure que le script s'arrête en cas d'erreur
set -e

# Lancer uvicorn
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000