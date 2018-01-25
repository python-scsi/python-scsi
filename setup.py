# coding: utf-8

from sys import platform
from distutils.command.build import build as _build
from distutils.core import setup, Extension


linux_sgio_module = Extension(name='linux_sgio.linux_sgio',
                              sources=['linux_sgio/sgiomodule.c'])

libiscsi_module = Extension(name='libiscsi._libiscsi',
                            sources=['libiscsi/libiscsi_wrap.c'],
                            libraries=['iscsi'],)


class PyScsiBuildCommand(_build):

    user_options = _build.user_options + [
        ('with-sgio', None,
         'build pyscsi with sgio support'),
        ('with-libiscsi', None,
         'build pyscsi with libiscsi support'), ]

    def initialize_options(self):
        self.with_sgio = None
        self.with_libiscsi = None
        _build.initialize_options(self)

    def finalize_options(self):
        _build.finalize_options(self)

    def run(self):
        if self.with_sgio and platform[:5] == 'linux':
            self.announce('build with sgio support ...', 2)
            self.distribution.ext_modules.append(linux_sgio_module)
            print(self.distribution.packages)
            self.distribution.packages.append('linux_sgio')
            print(self.distribution.packages)
        else:
            self.announce('your system is not supported by this module!', 2)
        if self.with_libiscsi and platform[:5] == 'linux':
            self.announce('build with libiscsi support ...', 2)
            self.distribution.ext_modules.append(libiscsi_module)
            self.distribution.packages.append('libiscsi')
        _build.run(self)


setup_dict = {'name': 'PYSCSI',
              'version': '1.0',
              'license': 'LGPLv2.1',
              'author': 'Ronnie Sahlberg',
              'author_email': 'ronniesahlberg@gmail.com',
              'description': 'Module for calling SCSI devices from Python',
              'packages': ['pyscsi', 'pyscsi.pyscsi', 'pyscsi.utils', ],
              'ext_modules': [],
              'cmdclass': {'build': PyScsiBuildCommand, }}

setup(**setup_dict)

# setup(name='PYSCSI',
#           version='1.0',
#           license='LGPLv2.1',
#           author='Ronnie Sahlberg',
#           author_email='ronniesahlberg@gmail.com',
#           description='Module for calling SCSI devices from Python',
#           packages=['pyscsi', 'pyscsi.pyscsi', 'pyscsi.utils'])