# coding: utf-8

from setuptools import find_packages, setup

# lets prepare our initial setup
setup_dict = {'packages': find_packages(),
              'python_requires': '~=3.7',
              'extras_require': {'sgio': ['cython-sgio'],
                                 'iscsi': ['cython-iscsi'],
                                 },
              }

setup(**setup_dict)
