# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_write10 import Write10
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int
from tests.mock_device import MockDevice, MockSCSI


class CdbWrite10Test(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(sbc)) as s:
            s.blocksize = 512

            data = bytearray(27 * 512)

            w = s.write10(1024, 27, data)
            cdb = w.cdb
            self.assertEqual(cdb[0], s.device.opcodes.WRITE_10.value)
            self.assertEqual(cdb[1], 0)
            self.assertEqual(scsi_ba_to_int(cdb[2:6]), 1024)
            self.assertEqual(cdb[6], 0)
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 27)
            self.assertEqual(cdb[9], 0)
            cdb = w.unmarshall_cdb(cdb)
            self.assertEqual(cdb["opcode"], s.device.opcodes.WRITE_10.value)
            self.assertEqual(cdb["wrprotect"], 0)
            self.assertEqual(cdb["dpo"], 0)
            self.assertEqual(cdb["fua"], 0)
            self.assertEqual(cdb["lba"], 1024)
            self.assertEqual(cdb["group"], 0)
            self.assertEqual(cdb["tl"], 27)

            d = Write10.unmarshall_cdb(Write10.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

            w = s.write10(65536, 27, data, wrprotect=2, dpo=1, fua=1, group=19)
            cdb = w.cdb
            self.assertEqual(cdb[0], s.device.opcodes.WRITE_10.value)
            self.assertEqual(cdb[1], 0x58)
            self.assertEqual(scsi_ba_to_int(cdb[2:6]), 65536)
            self.assertEqual(cdb[6], 0x13)
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 27)
            self.assertEqual(cdb[9], 0)
            cdb = w.unmarshall_cdb(cdb)
            self.assertEqual(cdb["opcode"], s.device.opcodes.WRITE_10.value)
            self.assertEqual(cdb["wrprotect"], 2)
            self.assertEqual(cdb["dpo"], 1)
            self.assertEqual(cdb["fua"], 1)
            self.assertEqual(cdb["lba"], 65536)
            self.assertEqual(cdb["group"], 19)
            self.assertEqual(cdb["tl"], 27)

            d = Write10.unmarshall_cdb(Write10.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
