# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi import scsi_enum_modesense as MODESENSE10
from pyscsi.pyscsi.scsi_cdb_modesense10 import ModeSense10
from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.utils.converter import scsi_ba_to_int

from .mock_device import MockDevice, MockSCSI


class CdbModesense10Test(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(smc)) as s:
            # cdb for SMC: ElementAddressAssignment
            m = s.modesense10(page_code=MODESENSE10.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT)
            cdb = m.cdb
            self.assertEqual(cdb[0], s.device.opcodes.MODE_SENSE_10.value)
            self.assertEqual(cdb[1], 0)
            self.assertEqual(cdb[2], MODESENSE10.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT)
            self.assertEqual(cdb[3], 0)
            self.assertEqual(cdb[4:6], bytearray(2))
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 96)
            self.assertEqual(cdb[9], 0)
            cdb = m.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.MODE_SENSE_10.value)
            self.assertEqual(cdb['dbd'], 0)
            self.assertEqual(cdb['llbaa'], 0)
            self.assertEqual(cdb['page_code'], MODESENSE10.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT)
            self.assertEqual(cdb['pc'], 0)
            self.assertEqual(cdb['sub_page_code'], 0)
            self.assertEqual(cdb['alloc_len'], 96)

            d = ModeSense10.unmarshall_cdb(ModeSense10.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

            m = s.modesense10(page_code=0, sub_page_code=3, llbaa=1, dbd=1, pc=MODESENSE10.PC.DEFAULT, alloclen=90)
            cdb = m.cdb
            self.assertEqual(cdb[0], s.device.opcodes.MODE_SENSE_10.value)
            self.assertEqual(cdb[1], 0x18)
            self.assertEqual(cdb[2], MODESENSE10.PC.DEFAULT << 6)
            self.assertEqual(cdb[3], 3)
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 90)
            cdb = m.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.MODE_SENSE_10.value)
            self.assertEqual(cdb['dbd'], 1)
            self.assertEqual(cdb['pc'], MODESENSE10.PC.DEFAULT)
            self.assertEqual(cdb['page_code'], 0)
            self.assertEqual(cdb['sub_page_code'], 3)
            self.assertEqual(cdb['alloc_len'], 90)
            self.assertEqual(cdb['llbaa'], 1)

            d = ModeSense10.unmarshall_cdb(ModeSense10.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
