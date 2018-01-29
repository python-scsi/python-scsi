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

#
# SCSI PreventAllowMediumRemoval command and definitions
#


class PreventAllowMediumRemoval(SCSICommand):
    """
    A class to hold information from a PositionToElement command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'prevent': [0x03, 4], }

    def __init__(self,
                 opcode,
                 prevent=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param prevent: prevent can have a value between 0 and 3
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             0)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  prevent=prevent)
