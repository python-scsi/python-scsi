# coding: utf-8

from setuptools import find_packages, setup

setup(
    packages=find_packages(exclude=["tests"]),
    python_requires='~=3.7',
    extras_require={
        'dev': ['isort', 'mypy', 'pre-commit', 'pytest', 'pytest-mypy'],
        'iscsi': ['cython-iscsi'],
        'sgio': ['cython-sgio'],
    },
)
