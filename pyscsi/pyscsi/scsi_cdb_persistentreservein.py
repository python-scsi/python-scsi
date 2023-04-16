# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# Copyright (C) 2023 by Brian Meagher<brian.meagher@ixsystems.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.pyscsi.scsi_enum_persistentreserve import *
from pyscsi.utils.converter import (
    decode_bits,
    encode_dict,
    scsi_ba_to_int,
    scsi_int_to_ba,
)

#
# SCSI PersistentReserveIn command and definitions
#
# It is impossible to determine PERSISTENT RESERVE IN service action has been
# issued merely by examining the response.  For example, the response to READ
# KEYS and READ RESERVATION will be identical if no keys are registered, or
# if no reservations are present.
#
# Therefore subclass PersistentReserveIn and have persistentreservein return
# the appropriate one
#

__all__ = [
    "PersistentReserveIn",
    "PersistentReserveInReadKeys",
    "PersistentReserveInReadReservation",
    "PersistentReserveInReportCapabilities",
    "PersistentReserveInReadFullStatus",
]


def _pad4_len(s):
    """
    Calculate the number of bytes necessary to hold the specified string incl a null
    terminator, padded to a multiple of 4 bytes
    """
    _l = len(s) + 1
    _rem = _l % 4
    if _rem:
        return _l + (4 - _rem)
    return _l


class PersistentReserveIn(SCSICommand):
    """
    A class to hold information from a PersistentReserveIn command to a scsi device
    """

    _cdb_bits = {
        "opcode": [0xFF, 0],
        "service_action": [0x1F, 1],
        "alloc_len": [0xFFFF, 7],
    }

    def __init__(self, opcode, service_action, alloclen=1024):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param service_action: service action code
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self, opcode, 0, alloclen)

        self.cdb = self.build_cdb(
            opcode=self.opcode.value, service_action=service_action, alloc_len=alloclen
        )


class PersistentReserveInReadKeys(PersistentReserveIn):
    """
    A class to hold information from a PersistentReserveIn command with
    READ KEYS service action.
    """

    _header_bits = {
        "pr_generation": [0xFFFFFFFF, 0],
        "additional_length": [0xFFFFFFFF, 4],
    }

    def __init__(self, opcode, alloclen=1024, **kwargs):
        PersistentReserveIn.__init__(
            self, opcode, opcode.serviceaction.READ_KEYS, alloclen
        )

    @classmethod
    def unmarshall_datain(cls, data):
        """
        Unmarshall the PersistentReserveInReadKeys datain.

        :param data: a byte array
        :return result: a dic
        """
        result = {}
        result["pr_generation"] = scsi_ba_to_int(data[:4])
        additional_length = scsi_ba_to_int(data[4:8])
        data = data[8 : additional_length + 8]
        keys = []
        while len(data):
            key = scsi_ba_to_int(data[:8])
            data = data[8:]
            keys.append(key)
        result["reservation_keys"] = keys
        return result


class PersistentReserveInReadReservation(PersistentReserveIn):
    """
    A class to hold information from a PersistentReserveIn command with
    READ RESERVATION service action.
    """

    _bits = {
        "reservation_key": [0xFFFFFFFFFFFFFFFF, 8],
        "scope": [0xF0, 21],
        "type": [0x0F, 21],
    }

    def __init__(self, opcode, alloclen=1024, **kwargs):
        PersistentReserveIn.__init__(
            self, opcode, opcode.serviceaction.READ_RESERVATION, alloclen
        )

    @classmethod
    def unmarshall_datain(cls, data):
        """
        Unmarshall the PersistentReserveInReadReservation datain.

        :param data: a byte array
        :return result: a dic
        """
        result = {}
        result["pr_generation"] = scsi_ba_to_int(data[:4])
        additional_length = scsi_ba_to_int(data[4:8])
        if additional_length == 0:
            return result
        elif additional_length != 16:
            raise ValueError("READ RESERVATION has incorrect additional length")
        decode_bits(data, cls._bits, result)
        return result


class PersistentReserveInReportCapabilities(PersistentReserveIn):
    """
    A class to hold information from a PersistentReserveIn command with
    REPORT CAPABILITIES service action.
    """

    _bits = {
        "length": [0xFFFF, 0],
        "ptpl_c": [0x01, 2],
        "atp_c": [0x04, 2],
        "sip_c": [0x08, 2],
        "crh": [0x10, 2],
        "rlr_c": [0x80, 2],
        "ptpl_a": [0x01, 3],
        "allow_commands": [0x70, 3],
        "tmv": [0x80, 3],
        "pr_type_mask": [0xFFFF, 4],
    }

    _pr_type_mask_bits = {
        "wr_ex": [0x02, 4],
        "ex_ac": [0x08, 4],
        "wr_ex_ro": [0x20, 4],
        "ex_ac_ro": [0x40, 4],
        "wr_ex_ar": [0x80, 4],
        "ex_ac_ar": [0x01, 5],
    }

    def __init__(self, opcode, alloclen=1024, **kwargs):
        PersistentReserveIn.__init__(
            self, opcode, opcode.serviceaction.REPORT_CAPABILITIES, alloclen
        )

    @classmethod
    def unmarshall_datain(cls, data):
        """
        Unmarshall the PersistentReserveInReportCapabilities datain.

        :param data: a byte array
        :return result: a dic
        """
        result = {}
        decode_bits(data, cls._bits, result)
        if result["length"] == 0:
            return {}
        elif result["length"] != 8:
            raise ValueError("REPORT CAPABILITIES has incorrect additional length")
        del result["length"]
        _r = {}
        decode_bits(data, cls._pr_type_mask_bits, _r)
        result["pr_type_mask"] = _r
        return result


class PersistentReserveInReadFullStatus(PersistentReserveIn):
    """
    A class to hold information from a PersistentReserveIn command with
    READ FULL STATUS service action.
    """

    _full_status_desc_bits = {
        "reservation_key": [0xFFFFFFFFFFFFFFFF, 0],
        "r_holder": [0x01, 12],
        "all_tg_pt": [0x02, 12],
        "scope": [0xF0, 13],
        "type": [0x0F, 13],
        "relative_target_port_id": [0xFFFF, 18],
        "additional_desc_length": [0xFFFFFFFF, 20],
    }

    _transport_id_bits = {
        "tpid_format": [0xC0, 0],
        "protocol_id": [0x0F, 0],
    }

    def __init__(self, opcode, alloclen=1024, **kwargs):
        PersistentReserveIn.__init__(
            self, opcode, opcode.serviceaction.READ_FULL_STATUS, alloclen
        )

    @classmethod
    def unmarshall_transport_id(cls, data):
        """
        static helper method to unmarshall TransportID data

        :param data: a byte array with TransportID data
        :return: a dict
        """
        _r = {}
        decode_bits(data, cls._transport_id_bits, _r)
        # Now decode the SCSI transport protocol specific data (SPC-5 7.6.4)
        # There may be scope for improvement here for protocol experts
        # equipped with the relevant standards, in the meantime return the
        # data
        _protocol_id = _r["protocol_id"]
        if _protocol_id == PROTOCOL_ID.FIBRE_CHANNEL:
            _r["n_port_name"] = data[8:16]
        elif _protocol_id == PROTOCOL_ID.IEEE_1394:
            _r["eui64_name"] = data[8:16]
        elif _protocol_id == PROTOCOL_ID.RDMA:
            _r["initiator_port_identifier"] = data[8:24]
        elif _protocol_id == PROTOCOL_ID.ISCSI:
            _al = scsi_ba_to_int(data[2:4])
            if _r["tpid_format"] == 0:
                # ISCSI NAME is null-terminated, null-padded
                _r["iscsi_name"] = data[4 : _al + 4].decode("utf-8").rstrip("\0")
            elif _r["tpid_format"] == 1:
                # ISCSI NAME is not null-terminated, but ISCSI INITIATOR SESSION ID is.
                _full_str = data[4 : _al + 4].decode("utf-8").rstrip("\0")
                (_r["iscsi_name"], _r["iscsi_initiator_session_id"]) = _full_str.split(
                    ",i,0x"
                )
            else:
                raise ValueError("Invalid TPID FORMAT: %s" % _r["tpid_format"])
        elif _protocol_id == PROTOCOL_ID.SAS:
            _r["sas_address"] = data[4:12]
        elif _protocol_id == PROTOCOL_ID.SOP:
            _r["routing_id"] = data[4:12]
        else:
            raise ValueError("Invalid PROTOCOL ID: %s" % _protocol_id)
        return _r

    @classmethod
    def marshall_transport_id(cls, data):
        """
        static helper method to marshall TransportID data

        :param data: a dict with TransportID data
        :return result: a byte array
        """
        _protocol_id = data["protocol_id"]
        if _protocol_id != PROTOCOL_ID.ISCSI:
            result = bytearray(24)
            encode_dict(data, cls._transport_id_bits, result)

        if _protocol_id == PROTOCOL_ID.FIBRE_CHANNEL:
            result[8:16] = data["n_port_name"][:8]
        elif _protocol_id == PROTOCOL_ID.IEEE_1394:
            result[8:16] = data["eui64_name"][:8]
        elif _protocol_id == PROTOCOL_ID.RDMA:
            result[8:24] = data["initiator_port_identifier"][:16]
        elif _protocol_id == PROTOCOL_ID.ISCSI:
            if data.get("tpid_format") and not data.get("iscsi_initiator_session_id"):
                raise ValueError("Must specify iscsi_initiator_session_id")
            if data.get("iscsi_initiator_session_id"):
                if not data.get("tpid_format"):
                    raise ValueError("Must specify tpid_format=1")
                _str = f"{data['iscsi_name']},i,0x{data['iscsi_initiator_session_id']}"
            else:
                _str = data["iscsi_name"]
            result = bytearray(4 + _pad4_len(_str))
            encode_dict(data, cls._transport_id_bits, result)
            result[2:4] = scsi_int_to_ba(len(result) - 4, 2)
            result[4 : len(_str) + 4] = _str.encode("utf-8")
        elif _protocol_id == PROTOCOL_ID.SAS:
            result[4:12] = data["sas_address"][:8]
        elif _protocol_id == PROTOCOL_ID.SOP:
            result[4:12] = data["routing_id"][:8]

        return result

    @classmethod
    def unmarshall_datain(cls, data):
        """
        Unmarshall the PersistentReserveInReadFullStatus datain.

        :param data: a byte array
        :return result: a dic
        """
        result = {}
        result["pr_generation"] = scsi_ba_to_int(data[:4])
        result["full_status"] = []
        additional_length = scsi_ba_to_int(data[4:8])
        if additional_length == 0:
            return result
        data = data[8 : additional_length + 8]
        while len(data):
            _status_desc = {}
            decode_bits(data, cls._full_status_desc_bits, _status_desc)
            data = data[24:]
            additional_desc_length = _status_desc["additional_desc_length"]
            del _status_desc["additional_desc_length"]
            if additional_desc_length > 0:
                _status_desc["transport_id"] = cls.unmarshall_transport_id(data)
                data = data[additional_desc_length:]
                result["full_status"].append(_status_desc)

        return result
