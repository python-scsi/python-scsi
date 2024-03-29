# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_read12 import Read12
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int
from tests.mock_device import MockDevice, MockSCSI


class CdbRead12Test(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(sbc)) as s:
            s.blocksize = 512

            r = s.read12(1024, 27)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.READ_12.value)
            self.assertEqual(cdb[1], 0)
            self.assertEqual(scsi_ba_to_int(cdb[2:6]), 1024)
            self.assertEqual(scsi_ba_to_int(cdb[6:10]), 27)
            self.assertEqual(cdb[10], 0)
            self.assertEqual(cdb[11], 0)
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(cdb["opcode"], s.device.opcodes.READ_12.value)
            self.assertEqual(cdb["rdprotect"], 0)
            self.assertEqual(cdb["dpo"], 0)
            self.assertEqual(cdb["fua"], 0)
            self.assertEqual(cdb["rarc"], 0)
            self.assertEqual(cdb["lba"], 1024)
            self.assertEqual(cdb["group"], 0)
            self.assertEqual(cdb["tl"], 27)

            d = Read12.unmarshall_cdb(Read12.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

            r = s.read12(1024, 27, rdprotect=2, dpo=1, fua=1, rarc=1, group=19)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.READ_12.value)
            self.assertEqual(cdb[1], 0x5C)
            self.assertEqual(scsi_ba_to_int(cdb[2:6]), 1024)
            self.assertEqual(scsi_ba_to_int(cdb[6:10]), 27)
            self.assertEqual(cdb[10], 0x13)
            self.assertEqual(cdb[11], 0)
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(cdb["opcode"], s.device.opcodes.READ_12.value)
            self.assertEqual(cdb["rdprotect"], 2)
            self.assertEqual(cdb["dpo"], 1)
            self.assertEqual(cdb["fua"], 1)
            self.assertEqual(cdb["rarc"], 1)
            self.assertEqual(cdb["lba"], 1024)
            self.assertEqual(cdb["group"], 19)
            self.assertEqual(cdb["tl"], 27)

            d = Read12.unmarshall_cdb(Read12.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
