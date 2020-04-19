# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_readcapacity16 import ReadCapacity16
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int

from .mock_device import MockDevice, MockSCSI


class CdbReadcapacity16Test(unittest.TestCase):
    def test_main(self):

        with MockSCSI(MockDevice(sbc)) as s:
            r = s.readcapacity16(alloclen=37)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.SBC_OPCODE_9E.value)
            self.assertEqual(cdb[1], s.device.opcodes.SBC_OPCODE_9E.serviceaction.READ_CAPACITY_16)
            self.assertEqual(cdb[2:10], bytearray(8))
            self.assertEqual(scsi_ba_to_int(cdb[10:14]), 37)
            self.assertEqual(cdb[14:16], bytearray(2))
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.SBC_OPCODE_9E.value)
            self.assertEqual(cdb['service_action'], s.device.opcodes.SBC_OPCODE_9E.serviceaction.READ_CAPACITY_16)
            self.assertEqual(cdb['alloc_len'], 37)

            d = ReadCapacity16.unmarshall_cdb(ReadCapacity16.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
