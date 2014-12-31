# coding: utf-8

from distutils.core import setup, Extension

setup(name='SGIO',
    version='1.0',
    license='LGPLv2.1',
    author='Ronnie Sahlberg',
    author_email='ronniesahlberg@gmail.com',
    description='Module for calling SCSI devices from Python',
    packages=['sgio', 'sgio.pyscsi', 'sgio.utils'])


linux_sgio_module = Extension('linux_sgio.linux_sgio',
                              sources=['linux_sgio/sgiomodule.c'])

setup(name='LINUX_SGIO',
    version='1.0',
    license='LGPLv2.1',
    author='Ronnie Sahlberg',
    author_email='ronniesahlberg@gmail.com',
    description='Module for calling Linux SG_IO devices',
    packages=['linux_sgio'],
      ext_modules=[linux_sgio_module])
