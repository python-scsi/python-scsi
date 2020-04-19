<!--
SPDX-FileCopyrightText: 2014 The python-scsi Authors

SPDX-License-Identifier: LGPL-2.1-or-later
-->

# Development Information

You can install all tools needed for developing the package by using
the `dev` extra:

    python-scsi $ pip install -e .[dev]

This will include test and verification tools, as well as all the
necessary packages to build a new release.

## pre-commit

This repository uses [pre-commit](https://pre-commit.com/) to maintain a
consistent codebase. The tool is installed as part of the `dev` extra.

To activate the pre-commit hooks, you should use:

    python-scsi $ pre-commit install

which will set up the hooks for the current repository.

## Unit Testing

The tests directory contain unit tests for python-scsi.

To run the tests:

    python-scsi $ pip install -e .[dev]
    python-scsi $ pytest --mypy

or use the make file:

    $ cd tests
    $ make

## Continuous Integration

[Travis CI](https://travis-ci.com/) is set up to run integration tests
for the repository. The configuration is in the `.travis.yml` file.

Travis will execute the whole testsuite (unittests and typechecking)
on the master branch as well as on each Pull Request.

## Releasing

[Setuptools](https://setuptools.readthedocs.io/) is used to create the
released packages:

    python-scsi $ pip install -e .[dev]
    python-scsi $ git clean -fxd
    python-scsi $ git tag -a python-scsi-X.Y.Z
    python-scsi $ python3 setup.py sdist bdist_wheel

The `git tag` command is used to tag the version that will be used by
[setuptools-scm](https://github.com/pypa/setuptools_scm/) to apply the
correct version information in the source and wheel packages.

The version to tag should be following [Semantic
Versioning](https://semver.org/) (SemVer).

For more details, see [Generating distribution
archives](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives).

## Repository Layout

The repository follows a (mostly) standard layout for Python repositories:

 * `.gitignore` is part of the repository configuration and is set to
   ignore generated files from Python testing and usage.
 * `.pre-commit-config.yaml` contains the configuration for
   [pre-commit](https://pre-commit.com/) and its hooks.
 * `.travis.yml` configures the continuous integration used to
   validate pull requests.
 * `mypy.ini` contains configuration for
   [mypy](https://github.com/python/mypy).
 * `setup.py` and `setup.cfg` contain configuration for
   [setuptools](https://setuptools.readthedocs.io/).
 * `pyproject.toml` contains [PEP
   518](https://www.python.org/dev/peps/pep-0518/) configuration for
   various tools.
 * `pyscsi` contains the source code of the module that is actually
   installed by pip.
 * `tools` and `examples` contain Python entrypoints showing usage of
   the library.
 * `tests` contains the unittest to validate the correctness of the
   library.
