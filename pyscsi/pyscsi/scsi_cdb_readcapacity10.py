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

from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.utils.converter import encode_dict, decode_bits

#
# SCSI ReadCapacity10 command and definitions
#


class ReadCapacity10(SCSICommand):
    """
    A class to hold information from a ReadCapacity(10) command to a scsi device
    """
    _cdb_bits =    {'opcode': [0xff, 0], }

    _datain_bits = {'returned_lba': [0xffffffff, 0],
                    'block_length': [0xffffffff, 4], }

    def __init__(self,
                 opcode,
                 alloclen=8):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             alloclen)

        self.cdb = self.build_cdb()

    def build_cdb(self):
        """
        Build a ReadCapacity10 CDB

        :return: a byte array representing a code descriptor block
        """
        cdb = {'opcode': self.opcode.value, }

        return self.marshall_cdb(cdb)

    def unmarshall(self):
        """
        wrapper method for the unmarshall_datain method.
        """
        self.result = self.unmarshall_datain(self.datain)

    @staticmethod
    def unmarshall_datain(data):
        """
        Unmarshall the ReadCapacity10 datain.

        :param data: a byte array
        :return result: a dict
        """
        result = {}
        decode_bits(data,
                    ReadCapacity10._datain_bits,
                    result)
        return result

    @staticmethod
    def marshall_datain(data):
        """
        Marshall the ReadCapacity10 datain.

        :param data: a dict
        :return result: a byte array
        """
        result = bytearray(8)
        encode_dict(data,
                    ReadCapacity10._datain_bits,
                    result)
        return result

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a ReadCapacity10 cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb,
                    ReadCapacity10._cdb_bits,
                    result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a ReadCapacity10 cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(10)
        encode_dict(cdb,
                    ReadCapacity10._cdb_bits,
                    result)
        return result
