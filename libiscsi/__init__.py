from libiscsi import *
# from sys import version_info as _swig_python_version_info
# if _swig_python_version_info >= (2, 7, 0):
#     def swig_import_helper():
#         import importlib
#         mname = '.'.join((__name__, '_libiscsi')).lstrip('.')
#         try:
#             return importlib.import_module(mname)
#         except ImportError:
#             return importlib.import_module('_libiscsi')
#     _libiscsi = swig_import_helper()
#     del swig_import_helper
# elif _swig_python_version_info >= (2, 6, 0):
#     def swig_import_helper():
#         from os.path import dirname
#         import imp
#         fp = None
#         try:
#             fp, pathname, description = imp.find_module('_libiscsi', [dirname(__file__)])
#         except ImportError:
#             import _libiscsi
#             return _libiscsi
#         if fp is not None:
#             try:
#                 _mod = imp.load_module('_libiscsi', fp, pathname, description)
#             finally:
#                 fp.close()
#             return _mod
#     _libiscsi = swig_import_helper()
#     del swig_import_helper
# else:
#     import _libiscsi
# del _swig_python_version_info