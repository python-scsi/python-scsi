#!/usr/bin/env python
# coding: utf-8
# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import unittest

from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.utils.converter import scsi_ba_to_int
from mock_device import MockDevice, MockSCSI
from pyscsi.pyscsi.scsi_cdb_initelementstatuswithrange import InitializeElementStatusWithRange


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

if __name__ == '__main__':
    unittest.main()
