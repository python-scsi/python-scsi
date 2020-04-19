# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_testunitready import TestUnitReady
from pyscsi.pyscsi.scsi_enum_command import sbc

from .mock_device import MockDevice, MockSCSI


class CdbTestunitreadyTest(unittest.TestCase):
    def test_main(self):

        with MockSCSI(MockDevice(sbc)) as s:
            w = s.testunitready()
            cdb = w.cdb
            self.assertEqual(cdb[0], s.device.opcodes.TEST_UNIT_READY.value)
            self.assertEqual(cdb[1], 0)
            self.assertEqual(cdb[2], 0)
            self.assertEqual(cdb[3], 0)
            self.assertEqual(cdb[4], 0)
            self.assertEqual(cdb[5], 0)
            cdb = w.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.TEST_UNIT_READY.value)

            d = TestUnitReady.unmarshall_cdb(TestUnitReady.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
