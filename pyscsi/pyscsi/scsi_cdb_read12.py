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
# SCSI Read12 command and definitions
#


class Read12(SCSICommand):
    """
    A class to send a Read(12) command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'rdprotect': [0xe0, 1],
                 'dpo': [0x10, 1],
                 'fua': [0x08, 1],
                 'rarc': [0x04, 1],
                 'lba': [0xffffffff, 2],
                 'tl': [0xffffffff, 6],
                 'group': [0x1f, 10], }

    def __init__(self, scsi, lba, tl, **kwargs):
        """
        initialize a new instance

        :param scsi: a SCSI object
        :param lba: Logical Block Address
        :param tl: transfer length
        :param kwargs: a list of keyword args including rdprotect, dpo, fua, rarc and group (all needed in the cdb)
        """
        if scsi.blocksize == 0:
            raise SCSICommand.MissingBlocksizeException

        SCSICommand.__init__(self, scsi, 0, scsi.blocksize * tl)
        self.cdb = self.build_cdb(lba, tl, **kwargs)
        self.execute()

    def build_cdb(self, lba, tl, rdprotect=0, dpo=0, fua=0, rarc=0, group=0):
        """
        Build a Read12 CDB

        :param lba: Logical Block Address
        :param tl: transfer length
        :param rdprotect: value to specify checking the returning status for the read command
        :param dpo: disable page out, can have a value 0f 0 or 1
        :param fua: force until access, can have a value of 0 or 1
        :param rarc: rebuild assist recovery control, can have a value of 0 or 1
        :param group: group number, can be 0 or greater
        """
        cdb = {
            'opcode': self.scsi.device.opcodes.READ_12.value,
            'lba': lba,
            'tl': tl,
            'rdprotect': rdprotect,
            'dpo': dpo,
            'fua': fua,
            'rarc': rarc,
            'group': group,
        }
        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a Read12 cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb, Read12._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a Read12 cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(12)
        encode_dict(cdb, Read12._cdb_bits, result)
        return result
