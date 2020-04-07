# coding: utf-8

from setuptools import find_packages, setup

# lets prepare our initial setup
setup_dict = {'name': 'PYSCSI',
              'version': '1.0',
              'license': 'LGPLv2.1',
              'author': 'Ronnie Sahlberg',
              'author_email': 'ronniesahlberg@gmail.com',
              'description': 'Module for calling SCSI devices from Python',
              'packages': find_packages(),
              'python_requires': '~=3.7',
              'extras_require': {'sgio': ['cython-sgio'],
                                 'iscsi': ['cython-iscsi'],
                                 },
              }

setup(**setup_dict)
