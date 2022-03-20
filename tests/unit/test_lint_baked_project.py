from contextlib import contextmanager
from itertools import product

import pytest
import sh
from cookiecutter.utils import rmtree

# Linter checks based on work done by cookiecutter-django
# https://github.com/pydanny/cookiecutter-django/blob/master/tests/test_cookiecutter_generation.py

TOX_LINTERS = [
    "py",
    "build",
    "bandit",
    "safety",
    "black",
    "black-run",
    "isort",
    "isort-run",
    "flake8",
    "pylint",
    "spelling",
    "mypy",
]
DATA_ANALYSIS_COMMANDS = ["install-kernel", "strip-notebooks", "run-notebooks", "check-notebooks", "lint-notebooks"]
OPTIONS = ["data_analysis", "check_dependencies_updates", "documentation"]
VALUES = ["y", "n"]

# Necessary to disable some pylint check from this point on because sh confuses pylint
# pylint:disable=too-many-function-args,unexpected-keyword-arg,no-member


@contextmanager
def bake_in_temp_dir_with_git(cookies, *args, **kwargs):
    """
    Init a git repository and install pre-commit in its hooks
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    sh.git("init", ".", _cwd=str(result.project))
    sh.git("add", ".", _cwd=str(result.project))
    sh.pre_commit("install", _cwd=str(result.project))

    try:
        yield result
    finally:
        rmtree(str(result.project))


@pytest.mark.parametrize("linter", TOX_LINTERS)
def test_tox_passes(linter, cookies):
    with bake_in_temp_dir_with_git(cookies=cookies) as result:
        sh.tox("-e", linter, _cwd=str(result.project))


@pytest.mark.parametrize("data_analysis, check_dependencies_updates, documentation", product(VALUES, VALUES, VALUES))
def test_black_passes(data_analysis, check_dependencies_updates, documentation, cookies):
    extra_context = {
        "data_analysis": data_analysis,
        "check_dependencies_updates": check_dependencies_updates,
        "documentation": documentation,
    }
    with bake_in_temp_dir_with_git(cookies=cookies, extra_context=extra_context) as result:
        sh.tox("-e", "black", _cwd=str(result.project))


def test_spelling_passes(cookies):
    # We only need to check when every possible file and documentation is there
    extra_context = {elt: "y" for elt in OPTIONS}
    with bake_in_temp_dir_with_git(cookies=cookies, extra_context=extra_context) as result:
        sh.tox("-e", "spelling", _cwd=str(result.project))


def test_build_docs(cookies):
    extra_context = {"documentation": "y"}
    with bake_in_temp_dir_with_git(cookies=cookies, extra_context=extra_context) as result:
        sh.tox("-e", "docs", _cwd=str(result.project))


@pytest.mark.parametrize("command", DATA_ANALYSIS_COMMANDS)
def test_data_analysis_commands(command, cookies):
    # "strip-notebooks" needs at least one notebook in the target folder
    # it works with an empty Jupyter Notebook
    extra_context = {"data_analysis": "y"}
    with bake_in_temp_dir_with_git(cookies=cookies, extra_context=extra_context) as result:
        if command == "run-notebooks":
            # Tox command "run-notebooks" needs a kernel to run (by default the same as the project name)
            sh.tox("-e", "install-kernel", _cwd=str(result.project))
        sh.tox("-e", command, _cwd=str(result.project))


PRECOMMIT_HOOKS = [
    "check-added-large-files",
    "check-ast",
    "check-json",
    "check-merge-conflict",
    "check-toml",
    "check-yaml",
    "detect-private-key",
    "end-of-file-fixer",
    "trailing-whitespace",
]  # Removed prettier from the hooks because it fails


@pytest.mark.parametrize("hook, options", product(PRECOMMIT_HOOKS, VALUES))
def test_pre_commit_passes(hook, options, cookies):
    # Only running hooks not already covered by tox, since those are in the end ran by tox as well
    extra_context = {elt: options for elt in OPTIONS}
    with bake_in_temp_dir_with_git(cookies=cookies, extra_context=extra_context) as result:
        sh.pre_commit("run", hook, "--all-files", _cwd=str(result.project))


@pytest.mark.parametrize("data_analysis, check_dependencies_updates, documentation", product(VALUES, VALUES, VALUES))
def test_prettier_passes(data_analysis, check_dependencies_updates, documentation, cookies):
    # Prettier is a linter for many file types including Markdown

    extra_context = {
        "data_analysis": data_analysis,
        "check_dependencies_updates": check_dependencies_updates,
        "documentation": documentation,
    }
    with bake_in_temp_dir_with_git(cookies=cookies, extra_context=extra_context) as result:
        sh.pre_commit("run", "prettier", "--all-files", _cwd=str(result.project))


@pytest.mark.parametrize("data_analysis, check_dependencies_updates, documentation", product(VALUES, VALUES, VALUES))
def test_end_of_file_combinations(data_analysis, check_dependencies_updates, documentation, cookies):
    extra_context = {
        "data_analysis": data_analysis,
        "check_dependencies_updates": check_dependencies_updates,
        "documentation": documentation,
    }
    with bake_in_temp_dir_with_git(cookies=cookies, extra_context=extra_context) as result:
        sh.pre_commit("run", "end-of-file-fixer", "--all-files", _cwd=str(result.project))
