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

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE
from pyscsi.utils.converter import scsi_int_to_ba, encode_dict, decode_bits

#
# SCSI Write10 command and definitions
#


class Write10(SCSICommand):
    """
    A class to send a Write(10) command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'wrprotect': [0xe0, 1],
                 'dpo': [0x10, 1],
                 'fua': [0x08, 1],
                 'lba': [0xffffffff, 2],
                 'group': [0x1f, 6],
                 'tl': [0xffff, 7]
    }

    def __init__(self, scsi, lba, tl, data, **kwargs):
        self.dataout = data
        SCSICommand.__init__(self, scsi, scsi.blocksize * tl, 0)
        self.cdb = self.build_cdb(lba, tl, **kwargs)
        self.execute()

    def build_cdb(self, lba, tl, wrprotect=0, dpo=0, fua=0, group=0):
        """
        Build a Write10 CDB
        """
        cdb = {
            'opcode': self.scsi.device.opcodes.WRITE_10.value,
            'lba': lba,
            'tl': tl,
            'wrprotect': wrprotect,
            'dpo': dpo,
            'fua': fua,
            'group': group,
        }
        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a Write10 cdb
        """
        result = {}
        decode_bits(cdb, Write10._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a Write10 cdb
        """
        result = bytearray(10)
        encode_dict(cdb, Write10._cdb_bits, result)
        return result
