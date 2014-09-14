# coding: utf-8

from distutils.core import setup, Extension
module1 = Extension('sgio.sgio',
                    sources = ['sgio/sgiomodule.c'])

setup (name = 'SGIO',
       version = '1.0',
       description = 'Module for calling ioctl(SG_IO)',
       packages=['sgio','sgio.pyscsi','sgio.tests'],
       ext_modules = [module1])

