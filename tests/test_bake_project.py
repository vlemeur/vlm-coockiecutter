import copy
from contextlib import contextmanager
from pathlib import Path

from cookiecutter.utils import rmtree

# These tests have been copied from Cookiecutter Pypackage :
# https://github.com/audreyfeldroy/cookiecutter-pypackage/blob/master/tests/test_bake_project.py

MANIFEST = "manifest.yml"

DEFAULT_LAYOUT = set(
    [
        ".github",
        ".vscode",
        ".gitignore",
        ".pre-commit-config.yaml",
        ".pylintrc",
        "CHANGELOG.md",
        "README.md",
        "vlm_python_cookiecutter",
        "pyproject.toml",
        "setup.cfg",
        "setup.py",
        "spelling",
        "tests",
        "tox.ini",
    ]
)

EXPECTED_RENDERED_FILES = set(
    [
        ".gitignore",
        ".pre-commit-config.yaml",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        "CHANGELOG.md",
        "README.md",
        "vlm_python_cookiecutter/__init__.py",
        "pyproject.toml",
        "setup.cfg",
        "setup.py",
        "tests/__init__.py",
        "tests/test_sanity.py",
        "tox.ini",
    ]
)

EXPECTED_WORKFLOWS = set([".github/workflows/tests.yaml"])


def no_curlies(filepath):
    """Utility to make sure no curly braces appear in a file.
    That is, was Jinja able to render everything?
    """
    with open(filepath, "r") as file:
        data = file.read()

    template_strings = ["{{", "}}", "{%", "%}"]

    template_strings_in_file = [s in data for s in template_strings]
    return not any(template_strings_in_file)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def test_bake_project_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:

        assert result.exit_code == 0
        assert result.exception is None
        assert result.project.basename == "vlm-python-cookiecutter"
        assert result.project.isdir()

        found_toplevel_files = {f.basename for f in result.project.listdir()}
        assert found_toplevel_files == DEFAULT_LAYOUT
        assert all(no_curlies(filepath=Path(result.project) / file) for file in EXPECTED_RENDERED_FILES)
        assert not all(no_curlies(filepath=Path(result.project) / file) for file in EXPECTED_WORKFLOWS)


def test_bake_project_with_special_characters(cookies):
    extra_context = {"full_name": "name 'quote' name"}
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:

        assert result.exit_code == 0
        assert result.exception is None
        assert result.project.basename == "vlm-python-cookiecutter"
        assert result.project.isdir()

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert set(found_toplevel_files) == DEFAULT_LAYOUT
        assert all(no_curlies(filepath=Path(result.project) / file) for file in EXPECTED_RENDERED_FILES)
        assert not all(no_curlies(filepath=Path(result.project) / file) for file in EXPECTED_WORKFLOWS)


def test_bake_project_with_data_analysis(cookies):
    extra_context = {"data_analysis": "y"}
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:

        assert result.exit_code == 0
        assert result.exception is None
        assert result.project.basename == "vlm-python-cookiecutter"
        assert result.project.isdir()

        data_analysis_layout = copy.copy(DEFAULT_LAYOUT)
        data_analysis_layout.update(["data", "notebooks", "pickles", "scripts"])

        found_toplevel_files = {f.basename for f in result.project.listdir()}
        assert found_toplevel_files == data_analysis_layout
        assert all(no_curlies(filepath=Path(result.project) / file) for file in EXPECTED_RENDERED_FILES)
        assert not all(no_curlies(filepath=Path(result.project) / file) for file in EXPECTED_WORKFLOWS)


def test_bake_project_with_documentation(cookies):
    extra_context = {"documentation": "y"}
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:

        assert result.exit_code == 0
        assert result.exception is None
        assert result.project.basename == "vlm-python-cookiecutter"
        assert result.project.isdir()
        documentation_layout = copy.copy(DEFAULT_LAYOUT)
        documentation_layout.update(["docs"])

        expected_workflows_documentation = copy.copy(EXPECTED_WORKFLOWS)
        expected_workflows_documentation.update([".github/workflows/release-doc.yaml"])

        found_toplevel_files = {f.basename for f in result.project.listdir()}
        assert found_toplevel_files == documentation_layout
        assert all(no_curlies(filepath=Path(result.project) / file) for file in EXPECTED_RENDERED_FILES)
        assert not all(no_curlies(filepath=Path(result.project) / file) for file in expected_workflows_documentation)
