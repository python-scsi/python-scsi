# coding: utf-8

# Copyright (C) 2016 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.utils.converter import (
    decode_bits,
    encode_dict,
    scsi_ba_to_int,
    scsi_int_to_ba,
)

#
# SCSI GetLBAStatus command and definitions
#


class ReportLuns(SCSICommand):
    """
    A class to hold information from a ReportLuns command to a scsi device
    """
    _cdb_bits =       {'opcode': [0xff, 0],
                       'select_report': [0xff, 2],
                       'alloc_len': [0xffffffff, 6], }

    _datain_bits =    {'lun': [0xffffffffffffffff, 0], }

    def __init__(self,
                 opcode,
                 report=0x00,
                 alloclen=96):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param report: select report field value
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             alloclen)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  select_report=report,
                                  alloc_len=alloclen)

    @classmethod
    def unmarshall_datain(cls, data):
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
            decode_bits(_data[:8],
                        cls._datain_bits,
                        _r)
            key = 'lun%s' % _count
            _r[key] = _r.pop('lun')
            _luns.append(_r)
            _data = _data[8:]
            _count += 1

        result.update({'luns': _luns})
        return result

    @classmethod
    def marshall_datain(cls, data):
        """
        Marshall the ReportLuns datain.

        :param data: a dict
        :return result: a byte array
        """
        result = bytearray(8)
        if 'luns' not in data:
            result[:4] = scsi_int_to_ba(len(result) - 4, 4)
            return result

        for l in data['luns']:
            _r = bytearray(8)
            encode_dict(l,
                        cls._datain_bits,
                        _r)

            result += _r
        result[:4] = scsi_int_to_ba(len(result) - 4, 4)
        return result
