# coding: utf-8

from sys import platform
from os import path as _path
from subprocess import check_call as _call
from subprocess import CalledProcessError

from distutils.command.build import build as _build
from setuptools import Extension, setup

try:
    from Cython.Build import cythonize

    src_extension = ".pyx"
except ImportError:
    src_extension = ".c"

    def cythonize(extensions):
        return extensions


# some helpers
libiscsi_path = _path.relpath(_path.join(_path.dirname(__file__), "libiscsi"))

libiscsi_cmd = "make -C %s" % libiscsi_path

# First we are going to build our ext_modules list. We assume that a
# normal install will build both Extentions!  To exclude them use the
# new build switches --without-sgio and without-libiscsi
linux_sgio_module = Extension(name='linux_sgio.linux_sgio',
                              sources=['linux_sgio/linux_sgio' + src_extension])

libiscsi_module = Extension(name='libiscsi._libiscsi',
                            sources=['libiscsi/libiscsi_wrap.c'],
                            libraries=['iscsi'],)

# TODO: write commands for every setup type so you can build the standard version with correct metadata
# TODO: for each package.


class PyScsiBuildCommand(_build):
    """
        Custom build command to provide  logic to remove or do stand-alone builds for sgio and libiscsi.

        The standard build will make a package that is called PYSCSI and it will include both linux_sgio
        and libiscsi. Its also possible to build PYSCSI without supporting LINUX_SGIO and/or LIBISCSI then
        you would end up with a plain PYSCSI package and you have to figure out how to talk to scsi devices
        by yourself.

        Note: If you build the stand-alone versions the metadata of the package gets changed to more specific
              information of the build package!

        :param --without-sgio: build pyscsi package without linux_sgio support
        :param --without-libiscsi: build pyscsi package without libiscsi support
        :param --only-sgio: build linux_sgio as stand-alone package without pyscsi
        :param --only-libiscsi: build libiscsi as stand-alone package without pyscsi
    """
    user_options = _build.user_options + [
        ('without-sgio', None,
         'build pyscsi without sgio support'),
        ('without-libiscsi', None,
         'build pyscsi without libiscsi support'),
        ('only-sgio', None,
         'build sgio as stand-alone package'),
        ('only-libiscsi', None,
         'build libiscsi as stand-alone package'),
    ]

    def initialize_options(self):
        self.without_sgio = None
        self.without_libiscsi = None
        self.only_sgio = None
        self.only_libiscsi = None
        _build.initialize_options(self)

    def finalize_options(self):
        # TODO: review this for sanity ...
        if self.only_sgio:
            self.without_libiscsi = 1
            self.only_libiscsi = 0
        elif self.only_libiscsi:
            self.without_sgio = 1
            self.only_sgio = 0
        else:
            pass
        _build.finalize_options(self)

    def run(self):
        self._check_extentions()
        self._check_stand_alone()
        _build.run(self)

    def _check_extentions(self):
        """
        Do some checks on the ext_modules.
        """
        if self.without_sgio:
            self._build_without_sgio()
        if self.without_libiscsi:
            self._build_without_libiscsi()
        else:
            try:
                self.announce('create libiscsi_wrap.c ...', 2)
                _call(libiscsi_cmd, shell=True)
            except CalledProcessError as e:
                self.announce('could not create libiscsi_wrap.c: %s' % e.message, 2)

    def _check_stand_alone(self):
        """
        Do some checks for stand-alone builds.
        """
        if self.only_sgio:
            self._build_sgio_standalone()
        if self.only_libiscsi:
            self._build_libiscsi_standalone()

    def _build_without_sgio(self):
        """
        Remove the LINUX_SGIO package from the build.
        """
        self.announce('build without sgio support ...', 2)
        index = self.distribution.ext_modules.index(linux_sgio_module)
        del self.distribution.ext_modules[index]
        index = self.distribution.packages.index('linux_sgio')
        del self.distribution.packages[index]

    def _build_without_libiscsi(self):
        """
        Remove the LIBISCSI Package from the build.
        """
        self.announce('build without libiscsi support ...', 2)
        index = self.distribution.ext_modules.index(libiscsi_module)
        del self.distribution.ext_modules[index]
        index = self.distribution.packages.index('libiscsi')
        del self.distribution.packages[index]

    def _build_sgio_standalone(self):
        """
        Prepare a stand-alone build for LINUX_SGIO.
        """
        self.announce('build without pyscsi support ...', 2)
        self.distribution.metadata.name = 'LINUX_SGIO'
        self.distribution.metadata.description = 'Module for calling Linux SG_IO devices'
        self._remove_pyscsi()

    def _build_libiscsi_standalone(self):
        """
        Prepare a stand-alone build for LIBISCSI.
        """
        self.announce('build without pyscsi support ...', 2)
        self.distribution.metadata.name = 'LIBISCSI'
        self.distribution.metadata.description = 'A libiscsi wrapper for pyscsi.'
        self._remove_pyscsi()

    def _remove_pyscsi(self):
        """
        Remove PYSCSI from the build.
        """
        for pkg in ['pyscsi','pyscsi.utils', 'pyscsi.pyscsi', 'pyscsi.pyiscsi']:
            del self.distribution.packages[self.distribution.packages.index(pkg)]


# lets prepare our initial setup
setup_dict = {'name': 'PYSCSI',
              'version': '1.0',
              'license': 'LGPLv2.1',
              'author': 'Ronnie Sahlberg',
              'author_email': 'ronniesahlberg@gmail.com',
              'description': 'Module for calling SCSI devices from Python',
              'packages': ['pyscsi', 'pyscsi.pyscsi', 'pyscsi.pyiscsi', 'pyscsi.utils', 'linux_sgio', 'libiscsi'],
              'ext_modules': cythonize([linux_sgio_module]),
              'cmdclass': {'build': PyScsiBuildCommand, }, }

# TODO: we might want to do a more sane check if we can build and install PYSCSI, LINUX_SGIO and LIBISCSI
if len(setup_dict['ext_modules']) > 0 and platform[:5] == 'linux':
    setup(**setup_dict)
elif len(setup_dict['ext_modules']) == 0:
    setup(**setup_dict)
else:
    print('your system is not supported by the sgio or libiscsi ...')
