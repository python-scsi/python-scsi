# coding: utf-8

# Copyright:
# Copyright (C) 2016 by Markus Rosjat<markus.rosjat@gmail.com>
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


class ReportLuns(SCSICommand):
    """
    A class to hold information from a ReportLuns command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'select_report': [0xff, 2],
                 'alloc_len': [0xffffffff, 6], }
    _datain_bits = {'lun': [0xffffffffffffffff, 0], }

    def __init__(self, scsi, report=0x00, alloclen=96):
        """
        initialize a new instance

        :param scsi: a SCSI instance
        :param report: select report field value
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self, scsi, 0, alloclen)
        self.cdb = self.build_cdb(report, alloclen)
        self.execute()

    def build_cdb(self, report, alloclen):
        """
        Build a ReportLuns CDB

        :param report: type of logical unit addresses that shall be reported
        :param alloclen: the max number of bytes allocated for the data_in buffer
        :return: a byte array representing a code descriptor block
        """
        cdb = {'opcode': self.scsi.device.opcodes.REPORT_LUNS.value,
               'select_report': report,
               'alloc_len': alloclen, }
        return self.marshall_cdb(cdb)

    def unmarshall(self):
        """
        wrapper method for the unmarshall_datain method.
        """
        self.result = self.unmarshall_datain(self.datain)

    @staticmethod
    def unmarshall_datain(data):
        """
        Unmarshall the ReportLuns datain buffer.

        :param data: a byte array
        :return result: a dic
        """
        result = {}
        _data = data[8:scsi_ba_to_int(data[:4]) + 4]
        _luns = []
        _count = 0
        while len(_data):
            #  maybe we drop the whole "put a dict into the list for every lun" thing at all
            _r = {}
            decode_bits(_data[:8], ReportLuns._datain_bits, _r)
            key = 'lun%s' % _count
            _r[key] = _r.pop('lun')
            _luns.append(_r)
            _data = _data[8:]
            _count += 1

        result.update({'luns': _luns})
        return result

    @staticmethod
    def marshall_datain(data):
        """
        Marshall the ReportLuns datain.

        :param data: a dict
        :return result: a byte array
        """
        result = bytearray(8)
        if not 'luns' in data:
            result[:4] = scsi_int_to_ba(len(result) - 4, 4)
            return result

        for l in data['luns']:
            _r = bytearray(8)
            encode_dict(l, ReportLuns._datain_bits, _r)
            result += _r

        result[:4] = scsi_int_to_ba(len(result) - 4, 4)
        return result

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a ReportLuns cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb, ReportLuns._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a ReportLuns cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(12)
        encode_dict(cdb, ReportLuns._cdb_bits, result)
        return result
