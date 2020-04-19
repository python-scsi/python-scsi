# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# Copyright (C) 2016 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_exception import SCSIDeviceCommandExceptionMeta as ExMETA
from pyscsi.utils.converter import CheckDict, decode_bits, encode_dict


class SCSICommand(metaclass=ExMETA):
    """
    The base class for a derived scsi command class
    """
    _cdb_bits: CheckDict = {}
    _cdb = None
    _sense = None
    _datain = None
    _dataout = None
    _result = None
    _page_code = None
    _opcode = None

    def __init__(self,
                 opcode,
                 dataout_alloclen,
                 datain_alloclen):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param dataout_alloclen: integer representing the size of the data_out buffer
        :param datain_alloclen: integer representing the size of the data_in buffer
        """
        # we need the _cdb_bits and _cdb values in staticmethods so we have to set it
        # on the class and not on the instance of the class. that might be wrong ...
        SCSICommand._cdb_bits = self._cdb_bits
        SCSICommand._cdb = SCSICommand.init_cdb(opcode)
        self.dataout = bytearray(dataout_alloclen)
        self.datain = bytearray(datain_alloclen)
        self.result = {}
        self.page_code = None
        self.opcode = opcode

    def __repr__(self):
        return self.__class__.__name__

    @staticmethod
    def init_cdb(opcode):
        """
        init a byte array representing a command descriptor block with fixed length
        depending on the Opcode

        :param opcode: a OpCode object
        :return: a byte array
        """
        if 0x00 <= opcode.value <= 0x1f:
            cdb = bytearray(6)
        elif 0x20 <= opcode.value <= 0x5f:
            cdb = bytearray(10)
        elif 0x00 <= opcode.value <= 0x1f:
            raise SCSICommand.OpcodeException
        elif 0x80 <= opcode.value <= 0x9f:
            cdb = bytearray(16)
        elif 0xa0 <= opcode.value <= 0xbf:
            cdb = bytearray(12)
        else:
            raise SCSICommand.OpcodeException
        return cdb

    @property
    def result(self):
        """
        getter method of the result property

        :return: a dictionary
        """
        return self._result

    @result.setter
    def result(self,
               value):
        """
        setter method of the result property

        :param value: a dictionary
        """
        self._result = value

    @property
    def cdb(self):
        """
        getter method of the cdb property

        :return: a byte array
        """
        return self._cdb

    @cdb.setter
    def cdb(self,
            value):
        """
        setter method of the cdb property

        :param value: a byte array
        """
        self._cdb = value

    @property
    def datain(self):
        """
        getter method of the datain property

        :return: a byte array
        """
        return self._datain

    @datain.setter
    def datain(self,
               value):
        """
        setter method of the datain property

        :param value: a byte array
        """
        self._datain = value

    @property
    def dataout(self):
        """
        getter method of the dataout property

        :return: a byte array
        """
        return self._dataout

    @dataout.setter
    def dataout(self,
                value):
        """
        setter method of the dataout property

        :param value: a byte array
        """
        self._dataout = value

    @property
    def sense(self):
        """
        getter method of the sense property

        :return: a byte array
        """
        return self._sense

    @sense.setter
    def sense(self,
              value):
        """
        setter method of the sense property

        :param value: a byte array
        """
        self._sense = value

    @property
    def pagecode(self):
        """
        getter method of the pagecode property
        """
        return self._page_code

    @pagecode.setter
    def pagecode(self,
                 value):
        """
        setter method of the pagecode property

        :param value: a hexadecimal
        """
        self._page_code = value

    @property
    def opcode(self):
        """
        getter method of the opcode property
        """
        return self._opcode

    @opcode.setter
    def opcode(self,
               value):
        """
        setter method of the opcode property

        :param value: a OpCode object
        """
        self._opcode = value

    def print_cdb(self):
        """
        simple helper to print out the cdb as hex values
        """

        for b in self._cdb:
            print('0x%02X ' % b)

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall an SCSICommand cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(len(SCSICommand._cdb))
        encode_dict(cdb,
                    SCSICommand._cdb_bits,
                    result)
        return result

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall an SCSICommand cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb,
                    SCSICommand._cdb_bits,
                    result)
        return result

    def build_cdb(self,
                  **kwargs):
        """
        Build a SCSICommand CDB

        :param kwargs: keyword argument dict, content depends on SCSICommand subclass
        :return: a byte array representing a code descriptor block
        """
        cdb = {key: kwargs[key] for key in kwargs.keys()}
        return SCSICommand.marshall_cdb(cdb)

    def unmarshall(self, **kwargs):
        """
        wrapper method for unmarshall_datain method.

        :param kwargs: keyword argument dict, content depends on SCSICommand subclass
        """
        try:
            if getattr(self,
                       'unmarshall_datain'):
                self.result = self.unmarshall_datain(self.datain, **kwargs)
        except AttributeError:
            raise NotImplementedError('%s has no method to unmarshall datain data' % self)
