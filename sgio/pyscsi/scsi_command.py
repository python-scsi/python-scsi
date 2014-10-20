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

from sgio.utils.enum import Enum
from sgio.pyscsi.scsi_exception import SCSICommandExceptionMeta as ExMETA
from sgio.pyscsi.scsi_exception import SCSIDeviceExceptionMeta as DeviceErrors


opcodes = {'INQUIRY':           0x12,
           'MODE_SENSE_6':      0x1a,
           'READ_10':           0x28,
           'READ_12':           0xa8,
           'READ_16':           0x88,
           'READ_CAPACITY_10':  0x25,
           'SERVICE_ACTION_IN': 0x9e,
           'TEST_UNIT_READY':   0x00,
           'WRITE_10':          0x2a,
           'WRITE_12':          0xaa,
           'WRITE_16':          0x8a,
           }

OPCODE = Enum(opcodes)

service_action_ins = {'READ_CAPACITY_16': 0x10, }

SERVICE_ACTION_IN = Enum(service_action_ins)

scsi_status = {'GOOD': 0x00,
               'CHECK_CONDITION': 0x02,
               'CONDITIONS_MET': 0x04,
               'BUSY': 0x08,
               'RESERVATION_CONFLICT': 0x18,
               'TASK_SET_FULL': 0x28,
               'ACA_ACTIVE': 0x30,
               'TASK_ABORTED': 0x40,
               'SGIO_ERROR': 0xff, }

SCSI_STATUS = Enum(scsi_status)


class SCSICommand(object):
    """
    The base class for a derived scsi command class
    """
    __metaclass__ = ExMETA

    def __init__(self, scsi, dataout_alloclen, datain_alloclen):
        """
        initialize a new instance

        :param dev: a SCSIDevice instance
        :param dataout_alloclen: integer representing the size of the data_out buffer
        :param datain_alloclen: integer representing the size of the data_in buffer
        """
        self.scsi = scsi
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
        except (DeviceErrors.CheckConditionError, DeviceErrors.SCSISGIOError) as e:
            print e
        else:
            if hasattr(self, 'unmarshall'):
                self.unmarshall()

    def decode_bits(self, data, check_dict):
        self.decode_bits_into_dict(data, check_dict, self.result)

    def decode_bits_into_dict(self, data, check_dict, dict):
        """
        helper method to perform some simple bit operations

        the list in the value of each key:value pair contains 2 values
         - the bit mask
         - thy byte number for the byte in the datain byte array

        for now we assume he have to right shift only

        :data: a buffer containing the bits to decode
        :check_dict: a dict with a list as value in each key:value pair
        """
        for key in check_dict.iterkeys():
            # get the values from dict
            bitmask, byte_pos = check_dict[key]
            value = data[byte_pos]
            while not bitmask & 0x01:
                bitmask >>= 1
                value >>= 1
            value &= bitmask
            self.add_result_to_dict(key, value, dict)

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

    def add_result(self, key, value):
        """
        method to update the result dictionary

        :param key: a string
        :param value: a byte or byte array
        """
        self.add_result_to_dict(key, value, self.result)

    def add_result_to_dict(self, key, value, dict):
        """
        method to update the result dictionary

        :param key: a string
        :param value: a byte or byte array
        """
        dict.update({key: value})
