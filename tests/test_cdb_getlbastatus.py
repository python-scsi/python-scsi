# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_getlbastatus import GetLBAStatus
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int

from .mock_device import MockDevice, MockSCSI


class CdbGetlbastatusTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(sbc)) as s:
            r = s.getlbastatus(19938722, alloclen=1112527)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.SBC_OPCODE_9E.value)
            self.assertEqual(cdb[1], s.device.opcodes.SBC_OPCODE_9E.serviceaction.GET_LBA_STATUS)
            self.assertEqual(scsi_ba_to_int(cdb[2:10]), 19938722)
            self.assertEqual(scsi_ba_to_int(cdb[10:14]), 1112527)
            self.assertEqual(cdb[14:16], bytearray(2))
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.SBC_OPCODE_9E.value)
            self.assertEqual(cdb['service_action'], s.device.opcodes.SBC_OPCODE_9E.serviceaction.GET_LBA_STATUS)
            self.assertEqual(cdb['lba'], 19938722)
            self.assertEqual(cdb['alloc_len'], 1112527)

            d = GetLBAStatus.unmarshall_cdb(GetLBAStatus.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
