# coding: utf-8

import sys

from setuptools import Extension, find_packages, setup

try:
    from Cython.Build import cythonize

    src_extension = ".pyx"
except ImportError:
    src_extension = ".c"

    def cythonize(extensions):
        return extensions

configured_extensions = []

if '--without-sgio' in sys.argv:
    sys.argv.remove('--without-sgio')
elif sys.platform[:5] == 'linux':
    configured_extensions.append(
        Extension(name='linux_sgio',
                  sources=['linux_sgio/linux_sgio' + src_extension]))

if '--without-libiscsi' in sys.argv:
    sys.argv.remove('--without-libiscsi')
else:
    configured_extensions.append(
        Extension(name='libiscsi',
                  sources=['libiscsi/libiscsi' + src_extension],
                  libraries=['iscsi']))


setup(
    name='PYSCSI',
    version='2',
    license='LGPLv2.1',
    author='Ronnie Sahlberg',
    author_email='ronniesahlberg@gmail.com',
    description='Module for calling SCSI devices from Python',
    packages=find_packages(),
    ext_modules=cythonize(configured_extensions)
)
