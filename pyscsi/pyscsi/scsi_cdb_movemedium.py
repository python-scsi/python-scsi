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
# SCSI MoveMedium command and definitions
#


class MoveMedium(SCSICommand):
    """
    A class to hold information from a MoveMedium command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'medium_transport_address': [0xffff, 2],
                 'source_address': [0xffff, 4],
                 'destination_address': [0xffff, 6],
                 'invert': [0x01, 10], }

    def __init__(self, scsi, xfer, source, dest, invert=0):
        """
        initialize a new instance

        :param scsi: a SCSI object
        :param xfer: medium transport address
        :param source: source address
        :param dest: destination address
        :param invert: invert can be 0 or 1
        """
        SCSICommand.__init__(self, scsi, 0, 0)
        self.cdb = self.build_cdb(xfer, source, dest, invert)
        self.execute()

    def build_cdb(self, xfer, source, dest, invert):
        """
        Build a MoveMedium CDB

        :param xfer: medium transport address
        :param source: source address
        :param dest: destination address
        :param invert: invert can be 0 or 1
        :return: a byte array representing a code descriptor block
        """
        cdb = {
            'opcode': self.scsi.device.opcodes.MOVE_MEDIUM.value,
            'medium_transport_address': xfer,
            'source_address': source,
            'destination_address': dest,
            'invert': invert
        }
        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a MoveMedium cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb, MoveMedium._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a MoveMedium cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(12)
        encode_dict(cdb, MoveMedium._cdb_bits, result)
        return result
