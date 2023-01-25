# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# Copyright (C) 2023 by Brian Meagher<brian.meagher@ixsystems.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_cdb_persistentreservein import PersistentReserveInReadFullStatus
from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.pyscsi.scsi_enum_persistentreserve import *
from pyscsi.utils.converter import (
    decode_bits,
    encode_dict,
    scsi_ba_to_int,
    scsi_int_to_ba,
)

#
# SCSI PersistentReserveOut command and definitions
#

__all__ = ["PersistentReserveOut"]


class PersistentReserveOut(SCSICommand):
    """
    A class to hold information from a PersistentReserveOut command to a scsi device
    """

    _cdb_bits = {
        "opcode": [0xFF, 0],
        "service_action": [0x1F, 1],
        "scope": [0xF0, 2],
        "pr_type": [0x0F, 2],
        "parameter_list_length": [0xFFFFFFFF, 5],
    }

    _basic_parameter_list_bits = {
        "reservation_key": [0xFFFFFFFFFFFFFFFF, 0],
        "service_action_reservation_key": [0xFFFFFFFFFFFFFFFF, 8],
        "spec_i_pt": [0x08, 20],
        "all_tg_pt": [0x04, 20],
        "aptpl": [0x01, 20],
    }

    _ram_parameter_list_bits = {
        "reservation_key": [0xFFFFFFFFFFFFFFFF, 0],
        "service_action_reservation_key": [0xFFFFFFFFFFFFFFFF, 8],
        "unreg": [0x02, 17],
        "aptpl": [0x01, 17],
        "relative_target_port_id": [0xFFFF, 18],
        "transportid_length": [0xFFFFFFFF, 20],
    }

    @classmethod
    def marshall_dataout(cls, opcode, service_action, data):
        """
        Marshall the PersistentReserveOut dataout.

        Depending on the service action, this will be either the 'Basic
        PERSISTENT RESERVE OUT parameter list' (SPC-5 6.17.3) or the
        'PERSISTENT RESERVE OUT command with REGISTER AND MOVE service action
        parameter list' (SPC-5 6.17.4)

        :param data: a dict with data
        :return result: a byte array
        """
        if service_action == opcode.serviceaction.REGISTER_AND_MOVE:
            _d = data.copy()
            result = bytearray(24)
            if _d.get("transport_id"):
                transportID = PersistentReserveInReadFullStatus.marshall_transport_id(
                    _d["transport_id"]
                )
                _d["transportid_length"] = len(transportID)
                encode_dict(_d, cls._ram_parameter_list_bits, result)
                return result + transportID
            else:
                _d["transportid_length"] = 0
                encode_dict(_d, cls._ram_parameter_list_bits, result)
                return result
        elif service_action == opcode.serviceaction.REGISTER and data.get("spec_i_pt"):
            result = bytearray(28)
            encode_dict(data, cls._basic_parameter_list_bits, result)
            transport_ids = []
            for t in data.get("transport_ids", []):
                transport_ids.append(
                    PersistentReserveInReadFullStatus.marshall_transport_id(t)
                )
            additional_parameter_data = b"".join(transport_ids)
            result[24:28] = scsi_int_to_ba(len(additional_parameter_data), 4)
            return result + additional_parameter_data
        else:
            result = bytearray(24)
            encode_dict(data, cls._basic_parameter_list_bits, result)
        return result

    def __init__(self, opcode, service_action, scope=0, pr_type=0, **kwargs):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param service_action: service action code
        :param scope: persistent reservation SCOPE field
        :param pr_type: persistent reservation TYPE field
        :param data: a dict holding parameter list items (Basic or Register and Move)
        """
        _d = PersistentReserveOut.marshall_dataout(opcode, service_action, kwargs)

        SCSICommand.__init__(self, opcode, 0, 0)

        self.dataout = _d

        self.cdb = self.build_cdb(
            opcode=self.opcode.value,
            service_action=service_action,
            scope=scope,
            pr_type=pr_type,
            parameter_list_length=len(_d),
        )
