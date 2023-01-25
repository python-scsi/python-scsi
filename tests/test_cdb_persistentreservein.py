# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# Copyright (C) 2023 by Brian Meagher <brian.meagher@ixsystems.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_persistentreservein import *
from pyscsi.pyscsi.scsi_enum_command import spc
from pyscsi.pyscsi.scsi_enum_persistentreserve import *
from pyscsi.pyscsi.scsi_enum_report_target_port_groups import DATA_FORMAT_TYPE
from pyscsi.utils.converter import scsi_ba_to_int
from tests.mock_device import MockDevice, MockSCSI


class CdbPersistentreserveinTest(unittest.TestCase):
    def check_report_capabilities(self, data, bit_set):
        result = PersistentReserveInReportCapabilities.unmarshall_datain(data)
        for k in ["ptpl_c", "atp_c", "sip_c", "crh", "rlr_c", "ptpl_a", "tmv"]:
            if k == bit_set:
                self.assertEqual(result[k], 1)
            else:
                self.assertEqual(result[k], 0)
        for k in ["wr_ex", "ex_ac", "wr_ex_ro", "ex_ac_ro", "wr_ex_ar", "ex_ac_ar"]:
            if k == bit_set:
                self.assertEqual(result["pr_type_mask"][k], 1)
            else:
                self.assertEqual(result["pr_type_mask"][k], 0)

    def test_main(self):

        key1_data = bytearray(b"\x00\x00\x00\x00\xDE\xAD\xBE\xEF")
        key2_data = bytearray(b"\xAB\xCD\xEF\xAA\xBB\xCC\xDD\xEE")
        key1_value = 0xDEADBEEF
        key2_value = 0xABCDEFAABBCCDDEE

        with MockSCSI(MockDevice(spc)) as s:
            # READ KEYS
            r = s.persistentreservein(service_action=0x00, alloclen=256)
            self.assertIsInstance(r, PersistentReserveInReadKeys)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.PERSISTENT_RESERVE_IN.value)
            self.assertEqual(
                cdb[1] & 0x1F,
                s.device.opcodes.PERSISTENT_RESERVE_IN.serviceaction.READ_KEYS,
            )
            self.assertEqual(cdb[2:6], bytearray(4))
            self.assertEqual(cdb[7], 1)
            self.assertEqual(cdb[8], 0)
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 256)
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(
                cdb["opcode"], s.device.opcodes.PERSISTENT_RESERVE_IN.value
            )
            self.assertEqual(
                cdb["service_action"],
                s.device.opcodes.PERSISTENT_RESERVE_IN.serviceaction.READ_KEYS,
            )
            self.assertEqual(cdb["alloc_len"], 256)
            d = PersistentReserveInReadKeys.unmarshall_cdb(
                PersistentReserveInReadKeys.marshall_cdb(cdb)
            )
            self.assertEqual(d, cdb)
            # READ KEYS unmarshall data - no keys
            result = PersistentReserveInReadKeys.unmarshall_datain(
                bytearray(b"\x00\x00\x00\x02\x00\x00\x00\x00")
            )
            self.assertEqual(result["pr_generation"], 2)
            self.assertEqual(len(result["reservation_keys"]), 0)
            # READ KEYS unmarshall data - one key
            data = bytearray(b"\x00\x00\x01\x00\x00\x00\x00\x08") + key1_data
            result = PersistentReserveInReadKeys.unmarshall_datain(data)
            self.assertEqual(result["pr_generation"], 256)
            self.assertEqual(len(result["reservation_keys"]), 1)
            # READ KEYS unmarshall data - one key
            data = (
                bytearray(b"\x01\x00\x00\x00\x00\x00\x00\x10") + key1_data + key2_data
            )
            result = PersistentReserveInReadKeys.unmarshall_datain(data)
            self.assertEqual(result["pr_generation"], 16777216)
            self.assertEqual(len(result["reservation_keys"]), 2)
            self.assertEqual(result["reservation_keys"][0], key1_value)
            self.assertEqual(result["reservation_keys"][1], key2_value)

            # READ RESERVATION
            r = s.persistentreservein(service_action=0x01, alloclen=255)
            self.assertIsInstance(r, PersistentReserveInReadReservation)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.PERSISTENT_RESERVE_IN.value)
            self.assertEqual(
                cdb[1] & 0x1F,
                s.device.opcodes.PERSISTENT_RESERVE_IN.serviceaction.READ_RESERVATION,
            )
            self.assertEqual(cdb[2:6], bytearray(4))
            self.assertEqual(cdb[7], 0)
            self.assertEqual(cdb[8], 0xFF)
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 255)
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(
                cdb["opcode"], s.device.opcodes.PERSISTENT_RESERVE_IN.value
            )
            self.assertEqual(
                cdb["service_action"],
                s.device.opcodes.PERSISTENT_RESERVE_IN.serviceaction.READ_RESERVATION,
            )
            self.assertEqual(cdb["alloc_len"], 255)
            d = PersistentReserveInReadReservation.unmarshall_cdb(
                PersistentReserveInReadReservation.marshall_cdb(cdb)
            )
            self.assertEqual(d, cdb)
            # READ RESERVATION unmarchall data - no reservation
            data = bytearray(b"\x00\x00\x00\x1f\x00\x00\x00\x00")
            result = PersistentReserveInReadReservation.unmarshall_datain(data)
            self.assertEqual(result["pr_generation"], 31)
            self.assertFalse("reservation_key" in result)
            self.assertFalse("scope" in result)
            self.assertFalse("type" in result)
            # READ RESERVATION unmarchall data - key1 reservation / Write Exclusive
            base = (
                bytearray(b"\x00\x00\x00\x20\x00\x00\x00\x10")
                + key1_data
                + bytearray(5)
            )
            result = PersistentReserveInReadReservation.unmarshall_datain(
                base + bytearray(b"\x01\x00\x00")
            )
            self.assertEqual(result["pr_generation"], 32)
            self.assertEqual(result["reservation_key"], key1_value)
            self.assertEqual(result["scope"], 0)
            self.assertEqual(result["type"], PR_TYPE.WRITE_EXCLUSIVE)
            # READ RESERVATION unmarchall data - key1 reservation / Exclusive Access
            result = PersistentReserveInReadReservation.unmarshall_datain(
                base + bytearray(b"\x03\x00\x00")
            )
            self.assertEqual(result["type"], PR_TYPE.EXCLUSIVE_ACCESS)

            # REPORT CAPABILITIES
            r = s.persistentreservein(service_action=0x02, alloclen=2048)
            self.assertIsInstance(r, PersistentReserveInReportCapabilities)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.PERSISTENT_RESERVE_IN.value)
            self.assertEqual(
                cdb[1] & 0x1F,
                s.device.opcodes.PERSISTENT_RESERVE_IN.serviceaction.REPORT_CAPABILITIES,
            )
            self.assertEqual(cdb[2:6], bytearray(4))
            self.assertEqual(cdb[7], 0x08)
            self.assertEqual(cdb[8], 0x00)
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 2048)
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(
                cdb["opcode"], s.device.opcodes.PERSISTENT_RESERVE_IN.value
            )
            self.assertEqual(
                cdb["service_action"],
                s.device.opcodes.PERSISTENT_RESERVE_IN.serviceaction.REPORT_CAPABILITIES,
            )
            self.assertEqual(cdb["alloc_len"], 2048)
            d = PersistentReserveInReportCapabilities.unmarshall_cdb(
                PersistentReserveInReportCapabilities.marshall_cdb(cdb)
            )
            self.assertEqual(d, cdb)
            # REPORT CAPABILITIES unmarshall data
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x00\x00\x00\x00\x00\x00"), ""
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x01\x00\x00\x00\x00\x00"), "ptpl_c"
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x04\x00\x00\x00\x00\x00"), "atp_c"
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x08\x00\x00\x00\x00\x00"), "sip_c"
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x10\x00\x00\x00\x00\x00"), "crh"
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x80\x00\x00\x00\x00\x00"), "rlr_c"
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x00\x01\x00\x00\x00\x00"), "ptpl_a"
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x00\x80\x00\x00\x00\x00"), "tmv"
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x00\x00\x02\x00\x00\x00"), "wr_ex"
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x00\x00\x08\x00\x00\x00"), "ex_ac"
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x00\x00\x20\x00\x00\x00"), "wr_ex_ro"
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x00\x00\x40\x00\x00\x00"), "ex_ac_ro"
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x00\x00\x80\x00\x00\x00"), "wr_ex_ar"
            )
            self.check_report_capabilities(
                bytearray(b"\x00\x08\x00\x00\x00\x01\x00\x00"), "ex_ac_ar"
            )
            result = PersistentReserveInReportCapabilities.unmarshall_datain(
                bytearray(b"\x00\x08\x00\x50\x00\x00\x00\x00")
            )
            self.assertEqual(result["allow_commands"], 5)

            # READ FULL STATUS
            r = s.persistentreservein(service_action=0x03, alloclen=512)
            self.assertIsInstance(r, PersistentReserveInReadFullStatus)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.PERSISTENT_RESERVE_IN.value)
            self.assertEqual(
                cdb[1] & 0x1F,
                s.device.opcodes.PERSISTENT_RESERVE_IN.serviceaction.READ_FULL_STATUS,
            )
            self.assertEqual(cdb[2:6], bytearray(4))
            self.assertEqual(cdb[7], 0x02)
            self.assertEqual(cdb[8], 0x00)
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 512)
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(
                cdb["opcode"], s.device.opcodes.PERSISTENT_RESERVE_IN.value
            )
            self.assertEqual(
                cdb["service_action"],
                s.device.opcodes.PERSISTENT_RESERVE_IN.serviceaction.READ_FULL_STATUS,
            )
            self.assertEqual(cdb["alloc_len"], 512)
            d = PersistentReserveInReadFullStatus.unmarshall_cdb(
                PersistentReserveInReadFullStatus.marshall_cdb(cdb)
            )
            self.assertEqual(d, cdb)

            # TransportID
            eight = bytearray(b"\x01\x02\x03\x04\x05\x06\x07\x08")
            sixteen = bytearray(
                b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
            )
            transport_id = {
                "protocol_id": PROTOCOL_ID.FIBRE_CHANNEL,
                "tpid_format": 0,
                "n_port_name": eight,
            }
            d = PersistentReserveInReadFullStatus.unmarshall_transport_id(
                PersistentReserveInReadFullStatus.marshall_transport_id(transport_id)
            )
            self.assertEqual(d, transport_id)

            transport_id = {
                "protocol_id": PROTOCOL_ID.IEEE_1394,
                "tpid_format": 0,
                "eui64_name": eight,
            }
            d = PersistentReserveInReadFullStatus.unmarshall_transport_id(
                PersistentReserveInReadFullStatus.marshall_transport_id(transport_id)
            )
            self.assertEqual(d, transport_id)

            transport_id = {
                "protocol_id": PROTOCOL_ID.RDMA,
                "tpid_format": 0,
                "initiator_port_identifier": sixteen,
            }
            d = PersistentReserveInReadFullStatus.unmarshall_transport_id(
                PersistentReserveInReadFullStatus.marshall_transport_id(transport_id)
            )
            self.assertEqual(d, transport_id)

            transport_id = {
                "protocol_id": PROTOCOL_ID.ISCSI,
                "tpid_format": 0,
                "iscsi_name": "iqn.1993-08.org.debian:01:90c27cf89279",
            }
            d = PersistentReserveInReadFullStatus.unmarshall_transport_id(
                PersistentReserveInReadFullStatus.marshall_transport_id(transport_id)
            )
            self.assertEqual(d, transport_id)

            transport_id = {
                "protocol_id": PROTOCOL_ID.ISCSI,
                "tpid_format": 1,
                "iscsi_name": "iqn.1993-08.org.debian:01:90c27cf89279",
                "iscsi_initiator_session_id": "1234567890",
            }
            d = PersistentReserveInReadFullStatus.unmarshall_transport_id(
                PersistentReserveInReadFullStatus.marshall_transport_id(transport_id)
            )
            self.assertEqual(d, transport_id)

            transport_id = {
                "protocol_id": PROTOCOL_ID.SAS,
                "tpid_format": 0,
                "sas_address": eight,
            }
            d = PersistentReserveInReadFullStatus.unmarshall_transport_id(
                PersistentReserveInReadFullStatus.marshall_transport_id(transport_id)
            )
            self.assertEqual(d, transport_id)

            transport_id = {
                "protocol_id": PROTOCOL_ID.SOP,
                "tpid_format": 0,
                "routing_id": eight,
            }
            d = PersistentReserveInReadFullStatus.unmarshall_transport_id(
                PersistentReserveInReadFullStatus.marshall_transport_id(transport_id)
            )
            self.assertEqual(d, transport_id)
