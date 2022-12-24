# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_readcd import ReadCd
from pyscsi.pyscsi.scsi_enum_command import mmc
from pyscsi.utils.converter import scsi_ba_to_int

from tests.mock_device import MockDevice, MockSCSI


class CdbRead10Test(unittest.TestCase):
    def test_main(self):

        with MockSCSI(MockDevice(mmc)) as s:
            r = s.readcd(lba=640, tl=2, est=1, dap=1, mcsb=0x10, c2ei=2, scsb=5)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.READ_CD.value)
            self.assertEqual(cdb[1], 0x06)
            self.assertEqual(scsi_ba_to_int(cdb[2:6]), 640)
            self.assertEqual(scsi_ba_to_int(cdb[6:9]), 2)
            self.assertEqual(cdb[9], 0x84)
            self.assertEqual(cdb[10], 0x05)
            self.assertEqual(cdb[11], 0x00)
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.READ_CD.value)
            self.assertEqual(cdb['lba'], 640)
            self.assertEqual(cdb['tl'], 2)
            self.assertEqual(cdb['est'], 1)
            self.assertEqual(cdb['dap'], 1)
            self.assertEqual(cdb['mcsb'], 0x10)
            self.assertEqual(cdb['c2ei'], 2)
            self.assertEqual(cdb['scsb'], 5)

            d = ReadCd.unmarshall_cdb(ReadCd.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

            r = s.readcd(lba=16384, tl=512, est=4, dap=0, mcsb=0x0a, c2ei=1, scsb=2)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.READ_CD.value)
            self.assertEqual(scsi_ba_to_int(cdb[2:6]), 16384)
            self.assertEqual(scsi_ba_to_int(cdb[6:9]), 512)
            self.assertEqual(cdb[9], 0x52)
            self.assertEqual(cdb[10], 0x02)
            self.assertEqual(cdb[11], 0x00)
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.READ_CD.value)
            self.assertEqual(cdb['lba'], 16384)
            self.assertEqual(cdb['tl'], 512)
            self.assertEqual(cdb['est'], 4)
            self.assertEqual(cdb['dap'], 0)
            self.assertEqual(cdb['mcsb'], 0x0a)
            self.assertEqual(cdb['c2ei'], 1)
            self.assertEqual(cdb['scsb'], 2)

            d = ReadCd.unmarshall_cdb(ReadCd.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
