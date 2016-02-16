# coding: utf-8

# Copyright:
#  Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
#  Copyright (C) 2016 by Diego Elio Pettenò <flameeyes@flameeyes.eu>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from pyscsi.pyscsi.scsi_sense import SCSICheckCondition


class SCSICommandExceptionMeta(type):
    """
    A meta class for class depending SCSICommand exceptions
    """
    def __new__(mcs, cls, bases, attributes):

        class CommandNotImplemented(Exception):
            pass

        class MissingBlocksizeException(Exception):
            pass

        class OpcodeException(Exception):
            pass

        attributes.update({'CommandNotImplemented': CommandNotImplemented})
        attributes.update({'MissingBlocksizeException': MissingBlocksizeException})
        attributes.update({'OpcodeException': OpcodeException})

        return type.__new__(mcs, cls, bases, attributes)


class SCSIDeviceExceptionMeta(type):
    """
    A meta class for class depending SCSICommand exceptions
    """
    def __new__(mcs, cls, bases, attributes):

        class CheckCondition(SCSICheckCondition):
            pass

        class SCSISGIOError(Exception):
            pass

        attributes.update({'CheckCondition': CheckCondition})
        attributes.update({'SCSISGIOError': SCSISGIOError})

        return type.__new__(mcs, cls, bases, attributes)


class SCSIDeviceCommandExceptionMeta(SCSICommandExceptionMeta, SCSIDeviceExceptionMeta):

    def __init__(cls, name, bases, attr):
        SCSICommandExceptionMeta.__init__(cls, name, bases, attr)
        SCSIDeviceExceptionMeta.__init__(cls, name, bases, attr)

    def __new__(mcs, name, bases, attr):
        t1 = SCSICommandExceptionMeta.__new__(mcs, name, bases, attr)
        name = t1.__name__
        bases = tuple(t1.mro())
        attr = t1.__dict__.copy()
        t2 = SCSIDeviceExceptionMeta.__new__(mcs, name, bases, attr)
        return t2
