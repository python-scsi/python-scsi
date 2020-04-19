# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_initelementstatuswithrange import (
    InitializeElementStatusWithRange,
)
from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.utils.converter import scsi_ba_to_int

from .mock_device import MockDevice, MockSCSI


class MockInitializeElementStatusWithRange(MockDevice):
    pass

class CdbInitelementstatuswithrangeTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(smc)) as s:
            r = s.initializeelementstatuswithrange(15, 3, rng=1, fast=1)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.INITIALIZE_ELEMENT_STATUS_WITH_RANGE.value)
            self.assertEqual(cdb[1], 0x03)
            self.assertEqual(scsi_ba_to_int(cdb[2:4]), 15)
            self.assertEqual(scsi_ba_to_int(cdb[6:8]), 3)

            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.INITIALIZE_ELEMENT_STATUS_WITH_RANGE.value)
            self.assertEqual(cdb['starting_element_address'], 15)
            self.assertEqual(cdb['number_of_elements'], 3)
            self.assertEqual(cdb['fast'], 1)
            self.assertEqual(cdb['range'], 1)

            d = InitializeElementStatusWithRange.unmarshall_cdb(InitializeElementStatusWithRange.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
