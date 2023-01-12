# coding: utf-8

# Copyright (C) 2023 by Brian Meagher<brian.meagher@ixsystems.com>
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
from pyscsi.pyscsi.scsi_enum_report_target_port_groups import DATA_FORMAT_TYPE

#
# SCSI ReportTargetPortGroups command and definitions
#


class ReportTargetPortGroups(SCSICommand):
    """
    A class to hold information from a ReportTargetPortGroups command to a scsi device
    """
    _cdb_bits =        {'opcode': [0xff, 0],
                        'service_action': [0x1f, 1],
                        'parameter_data_format': [0xe0, 1],
                        'alloc_len': [0xffffffff, 6], }

    _tpgd_bits =       {'asymmetric_access_state': [0x0f, 0],
                        'pref': [0x80, 0],
                        'ao_sup': [0x01, 1],
                        'an_sup': [0x02, 1],
                        's_sup': [0x04, 1],
                        'u_sup': [0x08, 1],
                        'o_sup': [0x40, 1],
                        't_sup': [0x80, 1],
                        'target_port_group': [0xffff, 2],
                        'status_code': [0xff, 5],
                        'vendor': [0xff, 6],
                        'target_port_count': [0xff, 7], }

    _ext_hdr_bits =    {'format_type': [0x70, 0],
                        'implicit_transition_time': [0xff, 1], }

    def __init__(self,
                 opcode,
                 data_format=DATA_FORMAT_TYPE.LENGTH_ONLY_HEADER_PARAMETER_DATA_FORMAT,
                 alloclen=16384):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param data_format: specifies the requested format for the parameter data returned
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             alloclen)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  service_action=self.opcode.serviceaction.REPORT_TARGET_PORT_GROUPS,
                                  parameter_data_format=data_format,
                                  alloc_len=alloclen)

    @classmethod
    def unmarshall_datain(cls, data):
        """
        Unmarshall the ReportTargetPortGroups datain.

        :param data: a byte array
        :return result: a dic
        """
        result = {}
        #  get the data after the return_data_length
        _data = data[4:scsi_ba_to_int(data[:4]) + 4]

        # Check whether length only or extended header parameter data format
        if len(_data) >= 4:
            _r = {}
            decode_bits(_data, cls._ext_hdr_bits, _r)
            result['format_type'] = _r['format_type']
            if _r['format_type'] == DATA_FORMAT_TYPE.EXTENDED_HEADER_PARAMETER_DATA_FORMAT:
                result['implicit_transition_time'] = _r['implicit_transition_time']
                _data = _data[4:]
        else:
            result['format_type'] = DATA_FORMAT_TYPE.LENGTH_ONLY_HEADER_PARAMETER_DATA_FORMAT

        _tpg_descriptors = []  # Target Port Group Descriptors
        while len(_data):
            _tpgd = {}  # Target Port Group Descriptor
            decode_bits(_data, cls._tpgd_bits, _tpgd)
            _data = _data[8:]

            _tp_descriptors = [] # Target Port Desxcriptors
            while len(_data) and len(_tp_descriptors) < _tpgd['target_port_count']:
                _tpd = {}  # Target Port Desxcriptor
                _tpd['relative_target_port_id'] = scsi_ba_to_int(_data[2:4])
                _tp_descriptors.append(_tpd)
                _data = _data[4:]

            _tpgd['target_ports'] = _tp_descriptors
            _tpg_descriptors.append(_tpgd)

        result.update({'target_port_group_descriptors': _tpg_descriptors, })
        return result

    @classmethod
    def marshall_datain(cls, data):
        """
        Marshall the ReportTargetPortGroups datain.

        :param data: a dict
        :return result: a byte array
        """
        result = bytearray(4)
        if 'format_type' in data and data['format_type'] == DATA_FORMAT_TYPE.EXTENDED_HEADER_PARAMETER_DATA_FORMAT:
            _r = bytearray(4)
            encode_dict(data, cls._ext_hdr_bits, _r)
            result += _r

        for _tpgd in data['target_port_group_descriptors']:
            _r = bytearray(8)
            encode_dict(_tpgd, cls._tpgd_bits, _r)
            result += _r
            for _tpd in _tpgd['relative_target_port_id']:
                result += bytearray(2)
                result += scsi_int_to_ba(_tpd['relative_target_port_id'], 2)

        result[:4] = scsi_int_to_ba(len(result) - 4, 4)
        return result
