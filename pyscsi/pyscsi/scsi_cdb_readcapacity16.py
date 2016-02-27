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
# SCSI ReadCapacity16 command and definitions
#


class ReadCapacity16(SCSICommand):
    """
    A class to hold information from a ReadCapacity(16) command to a scsi device
    """
    _cdb_bits =    {'opcode': [0xff, 0],
                    'service_action': [0x1f, 1],
                    'alloc_len': [0xffffffff, 10], }

    _datain_bits = {'returned_lba': [0xffffffffffffffff, 0],
                    'block_length': [0xffffffff, 8],
                    'p_type': [0x0e, 12],
                    'prot_en': [0x01, 12],
                    'p_i_exponent': [0xf0, 13],
                    'lbppbe': [0x0f, 13],
                    'lbpme': [0x80, 14],
                    'lbprz': [0x40, 14],
                    'lowest_aligned_lba': [0x3fff, 14], }

    def __init__(self,
                 opcode,
                 alloclen=32):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             alloclen)

        self.cdb = self.build_cdb(alloclen)

    def build_cdb(self,
                  alloclen):
        """
        Build a ReadCapacity16 CDB

        :param alloclen: the max number of bytes allocated for the data_in buffer
        :return: a byte array representing a code descriptor block
        """
        cdb = {'opcode': self.opcode.value,
               'service_action': self.opcode.serviceaction.READ_CAPACITY_16,
               'alloc_len': alloclen, }

        return self.marshall_cdb(cdb)

    def unmarshall(self):
        """
        wrapper method for the unmarshall_datain method.
        """
        self.result = self.unmarshall_datain(self.datain)

    @staticmethod
    def unmarshall_datain(data):
        """
        Unmarshall the ReadCapacity16 datain.

        :param data: a byte array
        :return result: a dict
        """
        result = {}
        decode_bits(data,
                    ReadCapacity16._datain_bits,
                    result)
        return result

    @staticmethod
    def marshall_datain(data):
        """
        Marshall the ReadCapacity16 datain.

        :param data: a dict
        :return result: a byte array
        """
        result = bytearray(32)
        encode_dict(data,
                    ReadCapacity16._datain_bits,
                    result)
        return result

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a ReadCapacity16 cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb,
                    ReadCapacity16._cdb_bits,
                    result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a ReadCapacity16 cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(16)
        encode_dict(cdb,
                    ReadCapacity16._cdb_bits,
                    result)
        return result
