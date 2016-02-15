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

    def __init__(self, scsi, lba, tl, data, **kwargs):
        if scsi.blocksize == 0:
            raise SCSICommand.MissingBlocksizeException

        SCSICommand.__init__(self, scsi, scsi.blocksize * tl, 0)
        self.dataout = data
        self.cdb = self.build_cdb(lba, tl, **kwargs)
        self.execute()

    def build_cdb(self, lba, tl, wrprotect=0, dpo=0, fua=0, group=0):
        """
        Build a Write16 CDB
        """
        cdb = {
            'opcode': self.scsi.device.opcodes.WRITE_16.value,
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
        Unmarshall a Write16 cdb
        """
        result = {}
        decode_bits(cdb, Write16._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a Write16 cdb
        """
        result = bytearray(16)
        encode_dict(cdb, Write16._cdb_bits, result)
        return result
