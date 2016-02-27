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
# SCSI Write16 command and definitions
#


class Write16(SCSICommand):
    """
    A class to send a Write(16) command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'wrprotect': [0xe0, 1],
                 'dpo': [0x10, 1],
                 'fua': [0x08, 1],
                 'lba': [0xffffffffffffffff, 2],
                 'group': [0x1f, 14],
                 'tl': [0xffffffff, 10], }

    def __init__(self,
                 opcode,
                 blocksize,
                 lba,
                 tl,
                 data,
                 **kwargs):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param blocksize: a blocksize
        :param lba: Logical Block Address
        :param tl: transfer length
        :param data: a byte array with data
        :param kwargs: a list of keyword args including wrprotect, dpo, fua and group (all needed in the cdb)
        """
        if blocksize == 0:
            raise SCSICommand.MissingBlocksizeException

        SCSICommand.__init__(self,
                             opcode,
                             blocksize * tl,
                             0)
        self.dataout = data
        self.cdb = self.build_cdb(lba,
                                  tl,
                                  **kwargs)

    def build_cdb(self,
                  lba,
                  tl,
                  wrprotect=0,
                  dpo=0,
                  fua=0,
                  group=0):
        """
        Build a Write16 CDB

        :param lba: Logical Block Address
        :param tl: transfer length
        :param wrprotect: value to specify write protection information
        :param dpo: disable page out, can have a value 0f 0 or 1
        :param fua: force until access, can have a value of 0 or 1
        :param group: group number, can be 0 or greater
        """
        cdb = {'opcode': self.opcode.value,
               'lba': lba,
               'tl': tl,
               'wrprotect': wrprotect,
               'dpo': dpo,
               'fua': fua,
               'group': group, }

        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a Write16 cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb,
                    Write16._cdb_bits,
                    result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a Write16 cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(16)
        encode_dict(cdb,
                    Write16._cdb_bits,
                    result)
        return result
