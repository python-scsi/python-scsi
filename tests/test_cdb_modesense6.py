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

from pyscsi.pyscsi.scsi_enum_command import spc
from pyscsi.pyscsi import scsi_enum_modesense as MODESENSE6
from pyscsi.pyscsi.scsi_cdb_modesense6 import ModeSense6
from mock_device import MockDevice, MockSCSI

class CdbModesense6Test(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(spc)) as s:
            # cdb for SMC: ElementAddressAssignment
            m = s.modesense6(page_code=MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT)
            cdb = m.cdb
            self.assertEqual(cdb[0], s.device.opcodes.MODE_SENSE_6.value)
            self.assertEqual(cdb[1], 0)
            self.assertEqual(cdb[2], MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT)
            self.assertEqual(cdb[3], 0)
            self.assertEqual(cdb[4], 96)
            self.assertEqual(cdb[5], 0)
            cdb = m.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.MODE_SENSE_6.value)
            self.assertEqual(cdb['dbd'], 0)
            self.assertEqual(cdb['pc'], 0)
            self.assertEqual(cdb['page_code'], MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT)
            self.assertEqual(cdb['sub_page_code'], 0)
            self.assertEqual(cdb['alloc_len'], 96)

            d = ModeSense6.unmarshall_cdb(ModeSense6.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

            m = s.modesense6(page_code=0, sub_page_code=3, dbd=1, pc=MODESENSE6.PC.DEFAULT, alloclen=90)
            cdb = m.cdb
            self.assertEqual(cdb[0], s.device.opcodes.MODE_SENSE_6.value)
            self.assertEqual(cdb[1], 0x08)
            self.assertEqual(cdb[2], MODESENSE6.PC.DEFAULT << 6)
            self.assertEqual(cdb[3], 3)
            self.assertEqual(cdb[4], 90)
            self.assertEqual(cdb[5], 0)
            cdb = m.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.MODE_SENSE_6.value)
            self.assertEqual(cdb['dbd'], 1)
            self.assertEqual(cdb['pc'], MODESENSE6.PC.DEFAULT)
            self.assertEqual(cdb['page_code'], 0)
            self.assertEqual(cdb['sub_page_code'], 3)
            self.assertEqual(cdb['alloc_len'], 90)

            d = ModeSense6.unmarshall_cdb(ModeSense6.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

if __name__ == '__main__':
    unittest.main()
