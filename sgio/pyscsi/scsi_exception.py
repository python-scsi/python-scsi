# coding: utf-8

from scsi_sense import SCSICheckCondition

class SCSICommandExceptionMeta(type):
    """A meta class for class depending SCSICommand exceptions

    """

    def __new__(mcs, cls, bases, attributes):

        class CommandNotImplemented(Exception):
            pass

        class OpcodeException(Exception):
            pass

        attributes.update({'CommandNotImplemented': CommandNotImplemented})
        attributes.update({'OpcodeException': OpcodeException})

        return type.__new__(mcs, cls, bases, attributes)


class SCSIDeviceExceptionMeta(type):
    """A meta class for class depending SCSICommand exceptions

    """

    def __new__(mcs, cls, bases, attributes):

        class CheckCondition(SCSICheckCondition):
            pass

        class SCSISGIOError(Exception):
            pass

        attributes.update({'CheckCondition': CheckCondition})
        attributes.update({'SCSISGIOError': SCSISGIOError})

        return type.__new__(mcs, cls, bases, attributes)