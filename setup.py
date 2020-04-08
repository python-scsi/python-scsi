# coding: utf-8

from setuptools import find_packages, setup

setup(
    packages=find_packages(),
    python_requires='~=3.7',
    extras_require={
        'dev': ['pytest'],
        'iscsi': ['cython-iscsi'],
        'sgio': ['cython-sgio'],
    },
)
