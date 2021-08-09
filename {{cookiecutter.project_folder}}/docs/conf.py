"""Sphinx configuration."""
project = "{{cookiecutter.package_name}}"
author = "{{cookiecutter.author}}"
copyright = f"2021, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_autodoc_typehints", "sphinx_rtd_theme"]
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"
