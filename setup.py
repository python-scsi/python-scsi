# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

# coding: utf-8

from setuptools import find_packages, setup

import setuptools_scm  # noqa: F401  # Ensure it's present.

setup(
    packages=find_packages(exclude=["tests"]),
    python_requires='~=3.7',
    extras_require={
        'dev': [
            'isort',
            'mypy',
            'pre-commit',
            'pytest',
            'pytest-mypy',
            'setuptools>=42',
            'setuptools_scm[toml]>=3.4',
            'wheel',
        ],
        'iscsi': ['cython-iscsi'],
        'sgio': ['cython-sgio'],
    },
)
