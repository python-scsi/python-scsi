# coding: utf-8

# Copyright:
# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
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
# SCSI PositionToElement command and definitions
#


class PositionToElement(SCSICommand):
    """
    A class to hold information from a PositionToElement command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'medium_transport_address': [0xffff, 2],
                 'destination_address': [0xffff, 4],
                 'invert': [0x01, 8], }

    def __init__(self, opcode, xfer, dest, invert=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param xfer: medium transport address
        :param dest: destination address
        :param invert: invert can be 0 or 1
        """
        SCSICommand.__init__(self, opcode, 0, 0)
        self.cdb = self.build_cdb(xfer, dest, invert)

    def build_cdb(self, xfer, dest, invert):
        """
        Build a PositionToElement CDB

        :param xfer: medium transport address
        :param dest: destination address
        :param invert: invert can be 0 or 1
        :return: a byte array representing a code descriptor block
        """
        cdb = {
            'opcode': self.opcode.value,
            'medium_transport_address': xfer,
            'destination_address': dest,
            'invert': invert
        }

        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a PositionToElement cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb, PositionToElement._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a PositionToElement cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(10)
        encode_dict(cdb, PositionToElement._cdb_bits, result)
        return result


