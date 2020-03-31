# coding: utf-8

import sys

from setuptools import find_packages, setup


setup(
    name='PYSCSI',
    version='2',
    license='LGPLv2.1',
    author='Ronnie Sahlberg',
    author_email='ronniesahlberg@gmail.com',
    description='Module for calling SCSI devices from Python',
    packages=find_packages(),
    python_requires="~=3.7",
    extras_require={
        "sgio": ["cython-sgio"],
        "iscsi": ["cython-iscsi"],
    }
)
