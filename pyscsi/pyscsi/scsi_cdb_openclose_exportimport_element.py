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

        self.cdb = self.build_cdb(xfer,
                                  acode)

    def build_cdb(self,
                  xfer,
                  acode):
        """
        Build a ExchangeMedium CDB

        :param xfer: element address
        :param acode: action code
        :return: a byte array representing a code descriptor block
        """
        cdb = {'opcode': self.opcode.value,
               'element_address': xfer,
               'action_code': acode, }

        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a OpenCloseImportExportElement cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb,
                    OpenCloseImportExportElement._cdb_bits,
                    result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a OpenCloseImportExportElement cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(6)
        encode_dict(cdb,
                    OpenCloseImportExportElement._cdb_bits,
                    result)
        return result
