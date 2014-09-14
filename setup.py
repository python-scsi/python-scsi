from distutils.core import setup, Extension

module1 = Extension('sgio',
                    sources = ['sgiomodule.c'])

setup (name = 'SGIO',
       version = '1.0',
       description = 'Module for calling ioctl(SG_IO)',
       ext_modules = [module1])

