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

from scsi_command import SCSICommand, OPCODE, SERVICE_ACTION_IN
from sgio.utils.converter import scsi_int_to_ba, scsi_ba_to_int
from sgio.utils.enum import Enum
#
# SCSI ReadCapacity16 command and definitions
#

readcapacity16_bits = {'p_type': [0x0e, 12],
                       'prot_en': [0x01, 12],
                       'p_i_exponent': [0xf0, 13],
                       'lbppbe': [0x0f, 13],
                       'lbpme': [0x80, 14],
                       'lbprz': [0x40, 14], }
#
# P_TYPE
#
p_types = {'TYPE_1_PROTECTION': 0x00,
           'TYPE_2_PROTECTION': 0x01,
           'TYPE_3_PROTECTION': 0x02, }

P_TYPE = Enum(p_types)


class ReadCapacity16(SCSICommand):
    """
    A class to hold information from a ReadCapacity(16) command to a scsi device
    """

    def __init__(self, scsi, alloclen=32):
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
        Build a ReadCapacity16 CDB

        :param alloclen: the max number of bytes allocated for the data_in buffer
        :return: a byte array representing a code descriptor block
        """
        cdb = SCSICommand.init_cdb(OPCODE.SERVICE_ACTION_IN)
        cdb[1] = SERVICE_ACTION_IN.READ_CAPACITY_16
        cdb[10:14] = scsi_int_to_ba(alloclen, 4)
        return cdb

    def unmarshall(self):
        """
        Unmarshall the ReadCapacity16 data.
        """
        self.add_result('returned_lba', scsi_ba_to_int(self.datain[0:8]))
        self.add_result('block_length', scsi_ba_to_int(self.datain[8:12]))
        self.decode_bits(self.datain, readcapacity16_bits)
        self.add_result('lowest_aligned_lba',
                        scsi_ba_to_int(self.datain[14:16]) & 0x3fff)
