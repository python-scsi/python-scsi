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

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE
from pyscsi.utils.converter import decode_bits

#
# SCSI ReadCapacity10 command and definitions
#


class ReadCapacity10(SCSICommand):
    """
    A class to hold information from a ReadCapacity(10) command to a scsi device
    """

    def __init__(self, scsi, alloclen=8):
        """
        initialize a new instance

        :param scsi: a SCSI instance
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self, scsi, 0, alloclen)
        self.cdb = self.build_cdb(alloclen)
        self.execute()

    def build_cdb(self, alloclen):
        """
        Build a ReadCapacity10 CDB

        :param alloclen: the max number of bytes allocated for the data_in buffer
        :return: a byte array representing a code descriptor block
        """
        cdb = self.init_cdb(self.scsi.device.opcodes.READ_CAPACITY_10.value)
        return cdb

    def unmarshall(self):
        """
        Unmarshall the ReadCapacity10 data.
        """
        _bits = {'returned_lba': [0xffffffff, 0],
                 'block_length': [0xffffffff, 4], }
        decode_bits(self.datain, _bits, self.result)

    def unmarshall_cdb(self, cdb):
        """
        method to unmarshall a byte array containing a cdb.
        """
        _tmp = {}
        _bits = {'opcode': [0xff, 0],
                 'rdprotect': [0xe0, 1],
                 'dpo': [0x10, 1],
                 'fua': [0x08, 1],
                 'rarc': [0x04, 1],
                 'lba': [0xffffffffffffffff, 2],
                 'group': [0x1f, 14],
                 'tl': [0xffffffff, 10], }
        decode_bits(cdb, _bits, _tmp)
        return _tmp
