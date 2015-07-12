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
# SCSI PreventAllowMediumRemoval command and definitions
#


class PreventAllowMediumRemoval(SCSICommand):
    """
    A class to hold information from a PositionToElement command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'prevent': [0x03, 8], }

    def __init__(self, scsi, prevent=0):
        """
        initialize a new instance

        :param scsi:
        :param prevent:
        """
        SCSICommand.__init__(self, scsi, 0, 0)
        self.cdb = self.build_cdb(prevent)
        self.execute()

    def build_cdb(self, prevent):
        """
        Build a PreventAllowMediumRemoval CDB

        :return: a byte array representing a code descriptor block
        """
        cdb = {
            'opcode': self.scsi.device.opcodes.PREVENT_ALLOW_MEDIUM_REMOVAL.value,
            'prevent': prevent, }

        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a PreventAllowMediumRemoval cdb
        """
        result = {}
        decode_bits(cdb, PreventAllowMediumRemoval._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a PreventAllowMediumRemoval cdb
        """
        result = bytearray(10)
        encode_dict(cdb, PreventAllowMediumRemoval._cdb_bits, result)
        return result
