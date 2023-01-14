# coding: utf-8

# Copyright (C) 2021 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import pyscsi.pyscsi.scsi_enum_readdiscinformation as rdi_enums
from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.utils.converter import decode_bits, encode_dict

#
# SCSI ReadDiscInformation command and definitions
#

# we get a generator for all readdiskinformation enums, so we can add them to the class
_enums = (
    (key, rdi_enums.__dict__[key])
    for key in rdi_enums.__dict__.keys()
    if key in rdi_enums.__all__ and key not in ["MODESENSE6"]
)


class ReadDiscInformation(SCSICommand):
    """
    A class to hold information from a ReadDiscInformation command to a scsi device
    """

    _cdb_bits = {
        "opcode": [0xFF, 0],
        "data_type": [0x07, 1],
        "alloc_len": [0xFFFF, 7],
    }

    for enum in _enums:
        setattr(SCSICommand, enum[0], enum[1])

    _sdi_bits = {
        "disc_information_length": [0xFFFF, 0],
        "disc_information_data_type": [0xE0, 2],
        "erasable": [0x10, 2],
        "state_of_last_session": [0x0C, 2],
        "disc_status": [0x03, 2],
        "number_of_first_track_on_disc": [0xFF, 3],
        "number_of_sessions_lsb": [0xFF, 4],
        "first_track_number_in_last_session_lsb": [0xFF, 5],
        "last_track_number_in_last_session_lsb": [0xFF, 6],
        "did_v": [0x80, 7],
        "dbc_v": [0x40, 7],
        "uru": [0x20, 7],
        "dac_v": [0x10, 7],
        "legacy": [0x04, 7],
        "bg_format_status": [0x03, 7],
        "disc_type": [0x03, 8],
        "number_of_sessions_msb": [0xFF, 9],
        "first_track_number_in_last_session_msb": [0xFF, 10],
        "last_track_number_in_last_session_msb": [0xFF, 11],
        "disc_identification": [0xFFFFFFFF, 12],
        "last_session_lead_in_start_address": ["b", 16, 4],
        "last_possible_lead_out_start_address": ["b", 20, 4],
        "disc_bar_code": ["b", 24, 8],
        "disc_application_code": [0xFF, 32],
        "number_of_opc_tables": [0xFF, 33],
    }
    _tri_bits = {
        "disc_information_length": [0xFFFF, 0],
        "disc_information_data_type": [0xE0, 2],
        "maximum_possible_number_of_the_tracks": [0xFFFF, 4],
        "number_of_the_assigned_tracks": [0xFFFF, 6],
        "maximum_possible_number_of_appendable_tracks": [0xFFFF, 8],
        "current_number_of_appendable_tracks": [0xFFFF, 10],
    }
    _pow_bits = {
        "disc_information_length": [0xFFFF, 0],
        "disc_information_data_type": [0xE0, 2],
        "remaining_pow_replacements": [0xFFFFFFFF, 4],
        "remaining_pow_reallocation_map_entries": [0xFFFFFFFF, 8],
        "number_of_remaining_pow_updates": [0xFFFFFFFF, 12],
    }

    def __init__(self, opcode, data_type, alloc_len=4096):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param data_type: Data Type
        :param alloc_len: Allocation Length
        """
        self._data_type = data_type
        SCSICommand.__init__(self, opcode, 0, alloc_len)

        self.cdb = self.build_cdb(
            opcode=self.opcode.value, data_type=data_type, alloc_len=alloc_len
        )

    @classmethod
    def unmarshall_datain(cls, data):
        """
        Unmarshall the ReadDiscInformation datain.

        :param data: a byte array
        :return result: a dict
        """
        result = {}
        if data[2] >> 5 == cls.DISC_INFORMATION_DATA_TYPE.STANDARD_DISC_INFORMATION:
            decode_bits(data, cls._sdi_bits, result)
            data = data[: result["disc_information_length"] + 2]
            result["number_of_sessions"] = (
                result["number_of_sessions_msb"] * 256
                + result["number_of_sessions_lsb"]
            )
            del result["number_of_sessions_msb"]
            del result["number_of_sessions_lsb"]
            result["first_track_number_in_last_session"] = (
                result["first_track_number_in_last_session_msb"] * 256
                + result["first_track_number_in_last_session_lsb"]
            )
            del result["first_track_number_in_last_session_msb"]
            del result["first_track_number_in_last_session_lsb"]
            result["last_track_number_in_last_session"] = (
                result["last_track_number_in_last_session_msb"] * 256
                + result["last_track_number_in_last_session_lsb"]
            )
            del result["last_track_number_in_last_session_msb"]
            del result["last_track_number_in_last_session_lsb"]
            return result
        if data[2] >> 5 == cls.DISC_INFORMATION_DATA_TYPE.TRACK_RESOURCES_INFORMATION:
            decode_bits(data, cls._tri_bits, result)
            return result
        if (
            data[2] >> 5
            == cls.DISC_INFORMATION_DATA_TYPE.POW_RESOURCES_DISC_INFORMATION
        ):
            decode_bits(data, cls._pow_bits, result)
            return result

        raise NotImplementedError(
            "Unknown disc information data type %d" % (data[2] >> 5)
        )
