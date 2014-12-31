# coding: utf-8


#      Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
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

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE
from pyscsi.utils.converter import scsi_int_to_ba, decode_bits

#
# SCSI MoveMedium command and definitions
#


class MoveMedium(SCSICommand):
    """
    A class to hold information from a MoveMedium command to a scsi device
    """

    def __init__(self, scsi, xfer, source, dest, invert=0):
        """
        initialize a new instance

        :param scsi: a SCSI instance
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self, scsi, 0, 0)
        self.cdb = self.build_cdb(xfer, source, dest, invert)
        self.execute()

    def build_cdb(self, xfer, source, dest, invert):
        """
        Build a MoveMedium CDB

        :return: a byte array representing a code descriptor block
        """
        cdb = SCSICommand.init_cdb(OPCODE.MOVE_MEDIUM)
        cdb[2:4] = scsi_int_to_ba(xfer, 2)
        cdb[4:6] = scsi_int_to_ba(source, 2)
        cdb[6:8] = scsi_int_to_ba(dest, 2)
        if invert:
            cdb[10] |= 0x01
        return cdb

    def unmarshall_cdb(self, cdb):
        """
        method to unmarshall a byte array containing a cdb.
        """
        _tmp = {}
        _bits = {'opcode': [0xff, 0],
                'medium_transport_address': [0xffff, 2],
                'source_address': [0xffff, 4],
                'destination_address': [0xffff, 6],
                'invert': [0x01, 10], }
        decode_bits(cdb, _bits, _tmp)
        return _tmp
