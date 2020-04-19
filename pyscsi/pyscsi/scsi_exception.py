# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# Copyright (C) 2016 by Diego Elio Pettenò <flameeyes@flameeyes.eu>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_sense import SCSICheckCondition


class SCSICommandExceptionMeta(type):
    """
    A meta class for class depending SCSICommand exceptions
    """
    def __new__(mcs,
                cls,
                bases,
                attributes):

        class CommandNotImplemented(Exception):
            pass

        class MissingBlocksizeException(Exception):
            pass

        class OpcodeException(Exception):
            pass

        attributes.update({'CommandNotImplemented': CommandNotImplemented})
        attributes.update({'MissingBlocksizeException': MissingBlocksizeException})
        attributes.update({'OpcodeException': OpcodeException})

        return type.__new__(mcs,
                            cls,
                            bases,
                            attributes)


class SCSIDeviceExceptionMeta(type):
    """
    A meta class for class depending SCSICommand exceptions
    """
    def __new__(mcs,
                cls,
                bases,
                attributes):

        class CheckCondition(SCSICheckCondition):
            pass

        attributes.update({'CheckCondition': CheckCondition})

        return type.__new__(mcs,
                            cls,
                            bases,
                            attributes)


class SCSIDeviceCommandExceptionMeta(SCSICommandExceptionMeta,
                                     SCSIDeviceExceptionMeta):

    def __init__(cls,
                 name,
                 bases,
                 attr):
        SCSICommandExceptionMeta.__init__(cls,
                                          name,
                                          bases,
                                          attr)
        SCSIDeviceExceptionMeta.__init__(cls,
                                         name,
                                         bases,
                                         attr)

    def __new__(mcs,
                name,
                bases,
                attr):
        t1 = SCSICommandExceptionMeta.__new__(mcs,
                                              name,
                                              bases,
                                              attr)
        name = t1.__name__
        bases = tuple(t1.mro())
        attr = t1.__dict__.copy()
        t2 = SCSIDeviceExceptionMeta.__new__(mcs,
                                             name,
                                             bases,
                                             attr)
        return t2
