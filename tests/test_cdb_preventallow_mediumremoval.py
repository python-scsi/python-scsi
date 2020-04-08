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

from pyscsi.pyscsi.scsi_cdb_preventallow_mediumremoval import PreventAllowMediumRemoval
from pyscsi.pyscsi.scsi_enum_command import smc

from .mock_device import MockDevice, MockSCSI


class CdbPreventallowMediumremovalTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(smc)) as s:
            m = s.preventallowmediumremoval(prevent=3)
            cdb = m.cdb
            self.assertEqual(cdb[0], s.device.opcodes.PREVENT_ALLOW_MEDIUM_REMOVAL.value)
            self.assertEqual(cdb[4], 0x03)
            cdb = m.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.PREVENT_ALLOW_MEDIUM_REMOVAL.value)
            self.assertEqual(cdb['prevent'], 3)

            d = PreventAllowMediumRemoval.unmarshall_cdb(PreventAllowMediumRemoval.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
