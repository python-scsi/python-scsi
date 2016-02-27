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
from pyscsi.utils.converter import scsi_int_to_ba, scsi_ba_to_int, encode_dict, decode_bits

#
# SCSI GetLBAStatus command and definitions
#


class GetLBAStatus(SCSICommand):
    """
    A class to hold information from a GetLBAStatus command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'service_action': [0x1f, 1],
                 'lba': [0xffffffffffffffff, 2],
                 'alloc_len': [0xffffffff, 10], }
    _datain_bits = {'lba': [0xffffffffffffffff, 0],
                    'num_blocks': [0xffffffff, 8],
                    'p_status': [0x0f, 12], }

    def __init__(self,
                 opcode,
                 lba,
                 alloclen=16384):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param lba: a local block address
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             alloclen)
        self.cdb = self.build_cdb(lba,
                                  alloclen)

    def build_cdb(self,
                  lba,
                  alloclen):
        """
        Build a GetLBAStatus CDB

        :param lba: starting local block address
        :param alloclen: the max number of bytes allocated for the data_in buffer
        :return: a byte array representing a code descriptor block
        """
        cdb = {'opcode': self.opcode.value,
               'service_action': self.opcode.serviceaction.GET_LBA_STATUS,
               'lba': lba,
               'alloc_len': alloclen, }
        return self.marshall_cdb(cdb)

    def unmarshall(self):
        """
        wrapper method for unmarshall_datain method.
        """
        self.result = self.unmarshall_datain(self.datain)

    @staticmethod
    def unmarshall_datain(data):
        """
        Unmarshall the GetLBAStatus datain.

        :param data: a byte array
        :return result: a dict
        """
        result = {}
        _data = data[8:scsi_ba_to_int(data[:4]) + 4]
        _lbas = []
        while len(_data):
            _r = {}
            decode_bits(_data[:16],
                        GetLBAStatus._datain_bits,
                        _r)

            _lbas.append(_r)
            _data = _data[16:]

        result.update({'lbas': _lbas})
        return result

    @staticmethod
    def marshall_datain(data):
        """
        Marshall the GetLBAStatus datain.

        :param data: a dict
        :return result: a byte array
        """
        result = bytearray(8)
        if not 'lbas' in data:
            result[:4] = scsi_int_to_ba(len(result) - 4, 4)
            return result

        for l in data['lbas']:
            _r = bytearray(16)
            encode_dict(l,
                        GetLBAStatus._datain_bits,
                        _r)

            result += _r

        result[:4] = scsi_int_to_ba(len(result) - 4, 4)
        return result

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a GetLBAStatus cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb,
                    GetLBAStatus._cdb_bits,
                    result)

        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a GetLBAStatus cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(16)
        encode_dict(cdb,
                    GetLBAStatus._cdb_bits,
                    result)

        return result
