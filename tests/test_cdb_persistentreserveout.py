# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# Copyright (C) 2023 by Brian Meagher <brian.meagher@ixsystems.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_persistentreserveout import *
from pyscsi.pyscsi.scsi_enum_command import spc
from pyscsi.pyscsi.scsi_enum_persistentreserve import *
from pyscsi.pyscsi.scsi_enum_report_target_port_groups import DATA_FORMAT_TYPE
from pyscsi.utils.converter import scsi_ba_to_int
from tests.mock_device import MockDevice, MockSCSI


class CdbPersistentreserveoutTest(unittest.TestCase):
    def test_main(self):

        key1_data = bytearray(b"\x00\x00\x00\x00\xDE\xAD\xBE\xEF")
        key2_data = bytearray(b"\xAB\xCD\xEF\xAA\xBB\xCC\xDD\xEE")
        key1_value = 0xDEADBEEF
        key2_value = 0xABCDEFAABBCCDDEE

        with MockSCSI(MockDevice(spc)) as s:
            # REGISTER
            r = s.persistentreserveout(service_action=0x00, scope=1, pr_type=4)
            self.assertIsInstance(r, PersistentReserveOut)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.PERSISTENT_RESERVE_OUT.value)
            self.assertEqual(
                cdb[1] & 0x1F,
                s.device.opcodes.PERSISTENT_RESERVE_OUT.serviceaction.REGISTER,
            )
            self.assertEqual(cdb[2], 0x14)
            self.assertEqual(cdb[3:5], bytearray(2))
            self.assertEqual(scsi_ba_to_int(cdb[5:9]), 24)
            self.assertEqual(cdb[9], 0)
            self.assertEqual(len(cdb), 10)
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(
                cdb["opcode"], s.device.opcodes.PERSISTENT_RESERVE_OUT.value
            )
            self.assertEqual(
                cdb["service_action"],
                s.device.opcodes.PERSISTENT_RESERVE_OUT.serviceaction.REGISTER,
            )
            self.assertEqual(cdb["scope"], 1)
            self.assertEqual(cdb["pr_type"], 4)
            d = PersistentReserveOut.unmarshall_cdb(
                PersistentReserveOut.marshall_cdb(cdb)
            )

            r = s.persistentreserveout(
                service_action=0x00, service_action_reservation_key=key2_value
            )
            self.assertEqual(r.cdb.hex(), "5f000000000000001800")
            self.assertEqual(len(r.dataout), 24)
            self.assertEqual(
                r.dataout.hex(), "0000000000000000abcdefaabbccddee0000000000000000"
            )

            r = s.persistentreserveout(
                service_action=0x00,
                service_action_reservation_key=key2_value,
                spec_i_pt=1,
            )
            self.assertEqual(
                r.dataout.hex(),
                "0000000000000000abcdefaabbccddee000000000800000000000000",
            )

            r = s.persistentreserveout(
                service_action=0x00,
                service_action_reservation_key=key2_value,
                all_tg_pt=1,
            )
            self.assertEqual(
                r.dataout.hex(), "0000000000000000abcdefaabbccddee0000000004000000"
            )

            r = s.persistentreserveout(
                service_action=0x00, service_action_reservation_key=key2_value, aptpl=1
            )
            self.assertEqual(
                r.dataout.hex(), "0000000000000000abcdefaabbccddee0000000001000000"
            )

            r = s.persistentreserveout(
                service_action=0x07,
                reservation_key=key2_value,
                service_action_reservation_key=0x0102030405060708,
                unreg=1,
                aptpl=1,
                relative_target_port_id=0xAABB,
            )
            self.assertEqual(r.cdb.hex(), "5f070000000000001800")
            self.assertEqual(len(r.dataout), 24)
            self.assertEqual(
                r.dataout.hex(), "abcdefaabbccddee01020304050607080003aabb00000000"
            )

            r = s.persistentreserveout(
                service_action=0x07,
                reservation_key=key2_value,
                service_action_reservation_key=0x0102030405060708,
                unreg=1,
                aptpl=1,
                relative_target_port_id=0xAABB,
                transport_id={
                    "protocol_id": PROTOCOL_ID.ISCSI,
                    "tpid_format": 0,
                    "iscsi_name": "iqn.1993-08.org.debian:01:90c27cf89279",
                },
            )
            self.assertEqual(r.cdb.hex(), "5f070000000000004400")
            tid = "0500002869716e2e313939332d30382e6f72672e64656269616e3a30313a3930633237636638393237390000"
            self.assertEqual(len(r.dataout), 68)
            self.assertEqual(
                r.dataout.hex(),
                "abcdefaabbccddee01020304050607080003aabb0000002c" + tid,
            )
