# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
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


class GetLBAStatus(SCSICommand):
    """
    A class to hold information from a GetLBAStatus command to a scsi device
    """
    _cdb_bits =    {'opcode': [0xff, 0],
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
        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  service_action=self.opcode.serviceaction.GET_LBA_STATUS,
                                  lba=lba,
                                  alloc_len=alloclen, )

    @classmethod
    def unmarshall_datain(cls,
                          data):
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
                        cls._datain_bits,
                        _r)

            _lbas.append(_r)
            _data = _data[16:]

        result.update({'lbas': _lbas})
        return result

    @classmethod
    def marshall_datain(cls, data):
        """
        Marshall the GetLBAStatus datain.

        :param data: a dict
        :return result: a byte array
        """
        result = bytearray(8)
        if 'lbas' not in data:
            result[:4] = scsi_int_to_ba(len(result) - 4, 4)
            return result

        for l in data['lbas']:
            _r = bytearray(16)
            encode_dict(l,
                        cls._datain_bits,
                        _r)

            result += _r

        result[:4] = scsi_int_to_ba(len(result) - 4, 4)
        return result
