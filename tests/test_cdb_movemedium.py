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
from .mock_device import MockDevice, MockSCSI
from pyscsi.pyscsi.scsi_cdb_movemedium import MoveMedium

class CdbMovemediumTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(smc)) as s:
            m = s.movemedium(15, 32, 64, invert=1)
            cdb = m.cdb
            self.assertEqual(cdb[0], s.device.opcodes.MOVE_MEDIUM.value)
            self.assertEqual(cdb[1], 0)
            self.assertEqual(scsi_ba_to_int(cdb[2:4]), 15)
            self.assertEqual(scsi_ba_to_int(cdb[4:6]), 32)
            self.assertEqual(scsi_ba_to_int(cdb[6:8]), 64)
            self.assertEqual(cdb[8], 0)
            self.assertEqual(cdb[9], 0)
            self.assertEqual(cdb[10], 0x01)
            cdb = m.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.MOVE_MEDIUM.value)
            self.assertEqual(cdb['medium_transport_address'], 15)
            self.assertEqual(cdb['source_address'], 32)
            self.assertEqual(cdb['destination_address'], 64)
            self.assertEqual(cdb['invert'], 1)

            d = MoveMedium.unmarshall_cdb(MoveMedium.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
