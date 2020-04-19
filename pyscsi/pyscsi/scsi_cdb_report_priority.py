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
# SCSI ReportPriority command and definitions
#


class ReportPriority(SCSICommand):
    """
    A class to hold information from a ReportPriority command to a scsi device
    """
    _cdb_bits =        {'opcode': [0xff, 0],
                        'service_action': [0x1f, 1],
                        'priority_reported': [0xc0, 2],
                        'alloc_len': [0xffffffff, 6], }

    _data_bits =       {'current_priority': [0x0f, 0],
                        'rtpi': [0xffff, 2],
                        'adlen': [0xffff, 6], }

    def __init__(self,
                 opcode,
                 priority=0,
                 alloclen=16384):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param priority: specifies information to be returned in data_in buffer
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             alloclen)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  service_action=self.opcode.serviceaction.REPORT_PRIORITY,
                                  priority_reported=priority,
                                  alloc_len=alloclen)

    @classmethod
    def unmarshall_datain(cls, data):
        """
        Unmarshall the ReportPriority datain.

        :param data: a byte array
        :return result: a dic
        """
        result = {}
        #  get the data after the ppd_len
        _data = data[4:scsi_ba_to_int(data[:4])]
        _descriptors = []
        while len(_data):
            _r = {}
            _dict = dict(cls._datain_bits.copy)
            _dict.update({'transport_id': [hex(scsi_ba_to_int(_data[6:7])), 8], })
            decode_bits(_data[:8 + scsi_ba_to_int(_data[6:7])],
                        _dict,
                        _r)
            _descriptors.append(_r)
            _data = _data[scsi_ba_to_int(_r['adlen']) + 8:]
        result.update({'priority_descriptors': _descriptors, })
        return result

    @classmethod
    def marshall_datain(cls, data):
        """
        Marshall the ReportPriority datain.

        :param data: a dict
        :return result: a byte array
        """
        result = bytearray(4)
        if 'priority_descriptors' not in data:
            result[:4] = scsi_int_to_ba(len(result), 4)
            return result

        for l in data['priority_descriptors']:
            _r = bytearray(len(l))
            _dict = dict(cls._datain_bits.copy)
            _dict.update({'transport_id': [hex(scsi_ba_to_int(len(l) - 8)), 8], })
            encode_dict(l, _dict, _r)
            result += _r

        result[:4] = scsi_int_to_ba(len(result), 4)
        return result
