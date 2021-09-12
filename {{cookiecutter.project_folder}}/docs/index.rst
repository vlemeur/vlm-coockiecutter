{{ cookiecutter.package_name }}
==============================

.. toctree::
   :hidden:
   :maxdepth: 1

   reference

Repository for the `{{ cookiecutter.package_name }}` library.


Installation
------------

The source code is stored on Jfrog and requires associated login and password.
Make sure `~/.pip/pip.conf` is configured.
Use the package manager `pip <https://pip.pypa.io/en/stable/>`_ to install mts_preprocessing.

.. code-block:: console

   $ pip install {{ cookiecutter.package_name }}

Quickstart
------------

.. code-block:: python

   $ import {{ cookiecutter.package_name }}
