# coding: utf-8


#      Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
#
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU Lesser General Public License as published by
#	   the Free Software Foundation; either version 2.1 of the License, or
#	   (at your option) any later version.
#
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU Lesser General Public License for more details.
#
#	   You should have received a copy of the GNU Lesser General Public License
#	   along with this program; if not, see <http://www.gnu.org/licenses/>.


class OPCODE(object):
    INQUIRY = 0x12

SCSI_STATUS_GOOD = 0x00
SCSI_STATUS_CHECK_CONDITION = 0x02
SCSI_STATUS_CONDITIONS_MET = 0x04
SCSI_STATUS_BUSY = 0x08
SCSI_STATUS_RESERVATION_CONFLICT = 0x18
SCSI_STATUS_TASK_SET_FULL = 0x28
SCSI_STATUS_ACA_ACTIVE = 0x30
SCSI_STATUS_TASK_ABORTED = 0x40
SCSI_STATUS_SGIO_ERROR = 0xff


def scsi_16_to_ba(i):
    """
    This function converts a 16-bit integer to a bytearray(2) in
    BigEndian byte order.

    i: a 16-bit integer
    return: a bytearray(2)
    """
    ba = bytearray(2)
    ba[0] = (i >> 8) & 0xff
    ba[1] = i & 0xff
    return ba


def scsi_32_to_ba(i):
    """
    This function converts a 32-bit integer to a bytearray(4) in
    BigEndian byte order.

    i: a 32-bit integer
    return: a bytearray(4)
    """
    ba = bytearray(4)
    ba[0] = (i >> 24) & 0xff
    ba[1] = (i >> 16) & 0xff
    ba[2] = (i >> 8) & 0xff
    ba[3] = i & 0xff
    return ba


def scsi_64_to_ba(i):
    """
    This function converts a 64-bit integer to a bytearray(8) in
    BigEndian byte order.

    i: a 64-bit integer
    return: a bytearray(8)
    """
    ba = bytearray(8)
    ba[0] = (i >> 56) & 0xff
    ba[1] = (i >> 48) & 0xff
    ba[2] = (i >> 40) & 0xff
    ba[3] = (i >> 32) & 0xff
    ba[4] = (i >> 24) & 0xff
    ba[5] = (i >> 16) & 0xff
    ba[6] = (i >> 8) & 0xff
    ba[7] = i & 0xff
    return ba


class SCSICommand(object):
    """
    The base class for a derived scsi command class
    """
    def __init__(self, dev, dataout_alloclen, datain_alloclen):
        """
        initialize a new instance

        :param dev: a SCSIDevice instance
        :param dataout_alloclen: integer representing the size of the data_out buffer
        :param datain_alloclen: integer representing the size of the data_in buffer
        """
        self.device = dev
        self.sense = bytearray(32)
        self.dataout = bytearray(dataout_alloclen)
        self.datain = bytearray(datain_alloclen)
        self.result = {}
        self.cdb = None
        self.pagecode = None

    @classmethod
    def init_cdb(cls, opcode):
        """
        init a byte array representing a command descriptor block with fixed length depending on the Opcode

        :param opcode: a byte
        :return: a byte array
        """
        if opcode < 0x20:
            cdb = bytearray(6)
        elif opcode < 0x60:
            cdb = bytearray(10)
        elif opcode < 0x80:
            raise OpcodeException
        elif opcode < 0xa0:
            cdb = bytearray(16)
        elif opcode < 0xc0:
            cdb = bytearray(12)
        else:
            raise OpcodeException

        cdb[0] = opcode
        return cdb

    def execute(self):
        """
        method to call the SCSIDevice.execute method

        this method takes no arguments but it calls the execute method of the device instance
        with the local attributes of the SCSICommand class.
        """
        self.device.execute(self.cdb, self.dataout, self.datain, self.sense)
        self.unmarshall()

    @property
    def result(self):
        """
        getter method of the result property

        :return: a dictionary
        """
        return self._result

    @result.setter
    def result(self, value):
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
    def cdb(self, value):
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
    def datain(self, value):
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
    def dataout(self, value):
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
    def sense(self, value):
        """
        setter method of the sense property

        :param value: a byte array
        """
        self._sense = value

    @property
    def device(self):
        """
        getter method of the cdb property

        :return: a SCSIDevice object
        """
        return self._device

    @device.setter
    def device(self, value):
        """
        setter method of the device property

        :param value: a SCSIDevice object
        """
        self._device = value

    @property
    def pagecode(self):
        return self._page_code

    @pagecode.setter
    def pagecode(self, value):
        self._page_code = value

    def add_result(self, key, value):
        """
        method to update the result dictionary

        :param key: a string
        :param value: a byte or byte array
        """
        self.result.update({key: value})
