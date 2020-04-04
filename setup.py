# coding: utf-8

from distutils.core import setup

# lets prepare our initial setup
setup_dict = {'name': 'PYSCSI',
              'version': '1.0',
              'license': 'LGPLv2.1',
              'author': 'Ronnie Sahlberg',
              'author_email': 'ronniesahlberg@gmail.com',
              'description': 'Module for calling SCSI devices from Python',
              'packages': ['pyscsi', 'pyscsi.pyscsi', 'pyscsi.pyiscsi', 'pyscsi.utils'],
              'extras_require': {'sgio': ['cython-sgio'],
                                 'iscsi': ['cython-iscsi'],
                                 },
              }

setup(**setup_dict)
