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
# SCSI WriteSame10 command and definitions
#


class WriteSame10(SCSICommand):
    """
    A class to send a WriteSame(10) command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'wrprotect': [0xe0, 1],
                 'anchor': [0x10, 1],
                 'unmap': [0x08, 1],
                 'lba': [0xffffffff, 2],
                 'group': [0x1f, 6],
                 'nb': [0xffff, 7], }

    def __init__(self,
                 opcode,
                 blocksize,
                 lba,
                 nb,
                 data,
                 wrprotect=0,
                 anchor=0,
                 unmap=0,
                 group=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param blocksize: a blocksize
        :param lba: logical block address
        :param nb: number of logical blocks
        :param data: a byte array with data
        :param wrprotect: value to specify write protection information
        :param anchor: anchor can have a value of 0 or 1
        :param unmap: unmap can have a value of 0 or 1
        :param group: group number, can be 0 or greater
        """
        if blocksize == 0:
            raise SCSICommand.MissingBlocksizeException

        SCSICommand.__init__(self,
                             opcode,
                             blocksize,
                             0)
        self.dataout = data
        self.cdb = self.build_cdb(lba,
                                  nb,
                                  wrprotect,
                                  anchor,
                                  unmap,
                                  group)

    def build_cdb(self,
                  lba,
                  nb,
                  wrprotect,
                  anchor,
                  unmap,
                  group):
        """
        Build a WriteSame10 CDB

        :param lba: logical block address
        :param nb: number of logical blocks
        :param wrprotect: value to specify write protection information
        :param anchor: anchor can have a value of 0 or 1
        :param unmap: unmap can have a value of 0 or 1
        :param group: group number, can be 0 or greater
        """
        cdb = {'opcode': self.opcode.value,
               'lba': lba,
               'nb': nb,
               'wrprotect': wrprotect,
               'anchor': anchor,
               'unmap': unmap,
               'group': group, }

        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a WriteSame10 cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb,
                    WriteSame10._cdb_bits,
                    result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a WriteSame10 cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(10)
        encode_dict(cdb,
                    WriteSame10._cdb_bits,
                    result)
        return result
