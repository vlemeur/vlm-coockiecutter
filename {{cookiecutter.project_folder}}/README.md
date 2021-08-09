# {{ cookiecutter.project_folder }}

{{ cookiecutter.project_short_description }}

## Installation

The source code is stored on Jfrog and requires associated login and password.
Make sure `~/.pip/pip.conf` is configured.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install {{ cookiecutter.package_name }}.

```bash
pip install {{ cookiecutter.package_name }}
```

## Quickstart

```python
import {{ cookiecutter.package_name }}
```

## Supported Python versions

## Dependencies

## Using tox to run linters and tests

- make sure you have created your `pip.conf` with proper JFrog credentials
- install tox: `pip install .[dev]` (This makes sure you install the currently supported version for `tox`)
- run a specific linter (using cache): `tox -e black`
- run a specific linter (without cache): `tox -r -e black`
- all available linter tox environments (to be called with `tox -e linter-name`) are: `build, bandit, black, black-run, isort, isort-run, flake8, pylint, spelling, update-spelling, mypy`
- Warning : installing the system dependency `enchant` is necessary to run tox environments `spelling` and `update-spelling` as well as their associated pre-commit hooks. See [spell checker usage](##-working-with-the-spell-checker) for more details.
- get the list of all the available tox environements with `tox -a`
- run all the tests with a specific python interpreter: `tox -e py37`
- run all the tests with your local python interpreter: `tox -e py`
- run all the tests with all supported python interpreters: `tox`
- (Use with caution) run all `tox` environments at once (it will prompt you for JFrog credentials for the release, do not give them): `tox -e ALL`

## Using pre-commit hooks

When contributing to this repository, you can activate pre-commit hooks to run linters on modified modules before you make a commit.

- Install the Python library `pre-commit`: `pip install .[dev]` (This makes sure you install the currently supported version for `pre-commit`)
- Run `pre-commit` once in order to generate pre-commit hooks in your git config: `pre-commit install`
- Every time you `git commit`, the linters and additional checks for config files will run and modify the files. In case no modifications were made to the files, the commit is done. Otherwise, you have to check the changes and `git add` and `git commit` again.
- Run all `pre-commit` checks without committing a single file: `pre-commit run --all-files`
- In order to bypass pre-commit checks on one commit: `git commit -m "No checks" --no-verify`
- In order to bypass pre-commit forever: `pre-commit uninstall`

## Process to release a new version of your package

- Create a dedicated branch (`bump-to-version-X.XX.XX`) and associated Pull Request on GitHub
- Update the version number everywhere in you project. Most of the time this means `setup.py`, but also `cruft.json` if you have used cruft to create/update the project.
- Update the [Changelog](CHANGELOG.md) according to [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- Merge the PR into master after review
- From master, in the GitHub web interface, create a new tag with the version number
- Deploy to JFrog is automated, enjoy !

## Working with `pylint`

`pylint` is a great tool to have shared best practices in the team and to help everyone produce better code.

However, we do realize it may be hard to comply to the rules set in the `.pylintrc` file for previous projects that have already accumulated months/years of development or for new client analysis projects.

There are different ways to relax `pylint` rules, from local to global disable. Note that this method applies to most linters, with different commands, but is mostly unnecessary for other more permissive or automated linters.

We recommend to try to disable rules locally first before removing them globally :

- Disabling pylint on a specific line, a specific block, a method, a module

  See the dedicated pylint documentation page : [Messages Control](http://pylint.pycqa.org/en/latest/user_guide/message-control.html#block-disables)

- Disabling pylint for the package or the tests

  You can edit the `pylint` arguments directly in the `tox.ini` file, allowing you to relax the rules only on the tests for example.

- Disabling pylint for the entire codebase (package & tests)

  If you want to disable a message or your entire project, you can edit the `pylint` config directly in `pylintrc`.

## Working with `mypy`

`mypy` is a great tool for static type checking of a library or service, however it might be too cumbersome for a client project.

Some resources to help you :

- Using types : [Type hints cheat sheet (Python 3)](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- Dealing with untyped dependencies : [Missing type hints for third party library](https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-type-hints-for-third-party-library)
- Locally silencing `mypy` the proper way : [Spurious errors and locally silencing the checker](https://mypy.readthedocs.io/en/stable/common_issues.html#spurious-errors-and-locally-silencing-the-checker)
- Other solutions to common issues : [Common issues and solutions](https://mypy.readthedocs.io/en/stable/common_issues.html#spurious-errors-and-locally-silencing-the-checker)

## Working with the spell checker
- The spell checker used for this project is [pyenchant](https://github.com/pyenchant/pyenchant) and it behaves pretty much as a pylint plugin.
- The only notable difference is you probably have to install a system library.
  On WSL/Ubuntu this would be `sudo apt-get install enchant`.
- This will install the English (US) dictionary, and a custom dictionary for python and metroscope words is provided at `spelling/spelling.txt`.
- Both dictionaries are used directly by the tox commands recomended below
- To check the current spelling of all project code, comments and docstrings, use `tox -e spelling`.
- If some words are correctly spelled yet are not accepted, you can update the custom dictionary yourself.
- Run `tox -e spelling-update` to append ALL the unknown words to the end of `spelling/spelling.txt`.
- Pick the words you would like to whitelist, run `tox -e spelling` to check and also to sort the list, then commit the new whitelist at `spelling/spelling.txt`

{% if cookiecutter.data_analysis == "y" -%}

## Recommended Notebook setup

- Outside of the project folder, create a virtual environment dedicated to Jupyter Lab that will be used to launch Jupyter from the terminal for all your projects:
  ```bash
  python3 -m venv jupyterlab
  source jupyterlab/bin/activate
  pip install jupyterlab
  ```
- Inside if the project folder, create a virtual environment dedicated to the project:
  ```bash
  cd {{ cookiecutter.project_folder }}
  python -m venv venv
  source venv/bin/activate
  pip install -U pip
  pip install -e ".[tests,dev,notebooks]"
  ```
- Create a Jupyter kernel for your project:
  ```bash
  source venv/bin/activate # if not already active
  ipython kernel install --user --name={{ cookiecutter.project_folder }}
  ```
- This kernel will now be accessible under the name `{{ cookiecutter.project_folder }}` in Jupyter Lab.
- If you do not use the recommended kernel name, please update the commands for testenv `run-notebooks` in [tox.ini](tox.ini).
- Please use `lab_black` for your Notebooks, by importing it at the top of your Notebooks:
  ```python
  %load_ext lab_black
  ```
- To strip all notebooks of their outputs: `tox -e strip-notebooks`
- To run all notebooks again to restore the outputs: `tox -e run-notebooks`
- You can easily adapt the commands if you need to run them only on a selection of notebooks. Commands can be found in [tox.ini](tox.ini).

{%- endif %}

{%- if cookiecutter.documentation == "y" -%}

## Building Documentation

Automated documentation is built with Sphinx from your project's docstrings.
Make sure to document functions, methods and classes with [NumpyDoc](https://numpydoc.readthedocs.io/en/latest/format.html).
Add your modules to the generated project's reference file at : `{{cookiecutter.project_folder}}/docs/reference.rst`
Documentation hosting is currently taken care of by the DevOps team once at the start of the project.
After that, hosted documentation is updated only on release (by default) and available only for the latest tag.
By default, documentation for `{{ cookiecutter.package_name }}` can be accessed with the Metroscope VPN only and at : `rnd.metroscope.io/{{ cookiecutter.package_name }}-doc`.
Once it's done, you can preview your documentation locally :

- build it with `tox -e docs`
- view the resulting html site by opening `docs/_build/index.html` in your favorite browser
- if you have the immense sadness of developing on WSL, use black magic or this VScode extension [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) to be able to view (dynamically) your WSL-bound documenation with a Windows-installed Browser.

{%- endif %}
