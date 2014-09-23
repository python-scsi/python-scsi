# coding: utf-8


class SCSICommandExceptionMeta(type):
    """A meta class for class depending SCSICommand exceptions

    """

    def __new__(meta, cls, bases, attributes):

        class CommandNotImplemented(Exception):
            pass

        class OpcodeException(Exception):
            pass

        attributes.update({'CommandNotImplemented': CommandNotImplemented})
        attributes.update({'OpcodeException': OpcodeException})

        return type.__new__(meta, cls, bases, attributes)