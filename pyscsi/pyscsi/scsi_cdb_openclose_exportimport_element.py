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
# SCSI OpenCloseImportExportElement command and definitions
#


class OpenCloseImportExportElement(SCSICommand):
    """
    A class to hold information from a OpenCloseImportExportElement
    command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'element_address': [0xffff, 2],
                 'action_code': [0x1f, 4], }

    def __init__(self,
                 opcode,
                 xfer,
                 acode,
                 **kwargs):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param xfer: element address
        :param acode: action code
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             0)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  element_address=xfer,
                                  action_code=acode, )
