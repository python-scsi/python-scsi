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

    def __init__(self, scsi, lba, nb, data, wrprotect=0, anchor=False,
                 unmap=False, group=0):
        SCSICommand.__init__(self, scsi, scsi.blocksize, 0)
        self.dataout = data
        self.cdb = self.build_cdb(lba, nb, wrprotect, anchor, unmap, group)
        self.execute()

    def build_cdb(self, lba, nb, wrprotect, anchor, unmap, group):
        """
        Build a WriteSame10 CDB
        """
        cdb = {
            'opcode': self.scsi.device.opcodes.WRITE_SAME_10.value,
            'lba': lba,
            'nb': nb,
            'wrprotect': wrprotect,
            'anchor': anchor,
            'unmap': unmap,
            'group': group,
        }
        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a WriteSame10 cdb
        """
        result = {}
        decode_bits(cdb, WriteSame10._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a WriteSame10 cdb
        """
        result = bytearray(10)
        encode_dict(cdb, WriteSame10._cdb_bits, result)
        return result

