# coding: utf-8

from distutils.core import setup, Extension

module_sgio = Extension('sgio.sgio',
                        sources=['sgio/sgiomodule.c'])

setup(name='SGIO',
    version='1.0',
    license='LGPLv2.1',
    author='Ronnie Sahlberg',
    author_email='ronniesahlberg@gmail.com',
    description='Module for calling ioctl(SG_IO)',
    packages=['sgio', 'sgio.pyscsi', 'sgio.tests', 'sgio.utils'],
      ext_modules=[module_sgio])

module_libiscsi = Extension('libiscsi.libiscsi',
                           sources=['libiscsi/libiscsimodule.c'])

setup(name='LIBISCSI',
    version='1.0',
    license='LGPLv2.1',
    author='Ronnie Sahlberg',
    author_email='ronniesahlberg@gmail.com',
    description='Module for calling libiscsi',
    packages=['libiscsi'],
      ext_modules=[module_libiscsi])
