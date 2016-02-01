# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
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


from pyscsi.pyscsi.scsi_exception import SCSIDeviceCommandExceptionMeta as ExMETA

# make a new base class with the metaclass this should solve the problem with the
# python 2 and python 3 metaclass definitions
_new_base_class = ExMETA('NewBaseClass', (object,), {})


class SCSICommand(_new_base_class):
    """
    The base class for a derived scsi command class
    """

    def __init__(self, scsi, dataout_alloclen, datain_alloclen):
        """
        initialize a new instance

        :param scsi: a SCSI instance
        :param dataout_alloclen: integer representing the size of the data_out buffer
        :param datain_alloclen: integer representing the size of the data_in buffer
        """
        self.scsi = scsi
        self._sense = bytearray(32)
        self._dataout = bytearray(dataout_alloclen)
        self._datain = bytearray(datain_alloclen)
        self._result = {}
        self._cdb = None
        self._page_code = None

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
            raise SCSICommand.OpcodeException
        elif opcode < 0xa0:
            cdb = bytearray(16)
        elif opcode < 0xc0:
            cdb = bytearray(12)
        else:
            raise SCSICommand.OpcodeException

        cdb[0] = opcode
        return cdb

    def execute(self):
        """
        method to call the SCSIDevice.execute method

        this method takes no arguments but it calls the execute method of the device instance
        with the local attributes of the SCSICommand class.
        """
        try:
            self.scsi.device.execute(self.cdb, self.dataout, self.datain, self.sense)
        except (self.CheckCondition, self.SCSISGIOError) as e:
            print(e)
        else:
            if hasattr(self, 'unmarshall'):
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
    def pagecode(self):
        """
        getter method of the pagecode property

        :return:
        """
        return self._page_code

    @pagecode.setter
    def pagecode(self, value):
        """
        setter method of the pagecode property

        :param value:
        :return:
        """
        self._page_code = value

    def print_cdb(self):
        for b in self._cdb:
            print('0x%02X ' % b)
