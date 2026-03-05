# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("../../"))

project = 'streamlit-app'
copyright = '2026, lvx'
author = 'lvx'

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",  # Pour extraire la doc du code
    "sphinx.ext.napoleon",  # Pour supporter les docstrings style
    "sphinx.ext.mathjax",  # Pour latex
    "sphinx.ext.viewcode",  # Pour afficher code source
    "myst_parser",  # Pour le markdown
    "sphinx_copybutton",  # Pour ajouter un bouton de copie
    "sphinxcontrib.mermaid", # Pour générer les schémas Mermaid
]

templates_path = ["_templates"]
exclude_patterns = []

language = "fr"

html_theme = "sphinx_rtd_theme"
html_logo = "_static/img/streamlit-logo.svg"
html_title = "Documentation - Sphinx - UV"
html_static_path = ["_static"]
