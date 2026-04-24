# coding: utf-8

# Copyright (C) 2026 by Brian Meagher<brian.meagher@truenas.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_unmap import Unmap
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int
from tests.mock_device import MockDevice, MockSCSI


class CdbUnmapTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(sbc)) as s:

            # Single descriptor, default flags
            u = s.unmap([{"lba": 0, "num_blocks": 0}])
            cdb = u.cdb
            self.assertEqual(cdb[0], s.device.opcodes.UNMAP.value)
            self.assertEqual(cdb[1], 0)  # anchor=0
            self.assertEqual(scsi_ba_to_int(cdb[2:6]), 0)  # reserved
            self.assertEqual(cdb[6], 0)  # group=0
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 24)  # 8 header + 16 descriptor
            self.assertEqual(cdb[9], 0)
            cdb = u.unmarshall_cdb(cdb)
            self.assertEqual(cdb["opcode"], s.device.opcodes.UNMAP.value)
            self.assertEqual(cdb["anchor"], 0)
            self.assertEqual(cdb["group"], 0)
            self.assertEqual(cdb["parameter_list_length"], 24)

            d = Unmap.unmarshall_cdb(Unmap.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

            # Single descriptor, anchor=1, group=0x3F, non-zero LBA and num_blocks
            u = s.unmap(
                [{"lba": 0x0102030405060708, "num_blocks": 0x090A0B0C}],
                anchor=1,
                group=0x3F,
            )
            cdb = u.cdb
            self.assertEqual(cdb[0], s.device.opcodes.UNMAP.value)
            self.assertEqual(cdb[1], 0x01)  # anchor=1
            self.assertEqual(scsi_ba_to_int(cdb[2:6]), 0)  # reserved
            self.assertEqual(cdb[6], 0x3F)  # group=63
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 24)
            self.assertEqual(cdb[9], 0)
            cdb = u.unmarshall_cdb(cdb)
            self.assertEqual(cdb["anchor"], 1)
            self.assertEqual(cdb["group"], 0x3F)
            self.assertEqual(cdb["parameter_list_length"], 24)

            d = Unmap.unmarshall_cdb(Unmap.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

            # Two descriptors — parameter_list_length = 8 + 2*16 = 40
            u = s.unmap(
                [{"lba": 0x100, "num_blocks": 0x10}, {"lba": 0x200, "num_blocks": 0x20}]
            )
            cdb = u.cdb
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 40)
            cdb = u.unmarshall_cdb(cdb)
            self.assertEqual(cdb["parameter_list_length"], 40)

    def test_dataout(self):
        with MockSCSI(MockDevice(sbc)) as s:

            # Single descriptor: verify parameter list bytes
            u = s.unmap([{"lba": 0x0102030405060708, "num_blocks": 0x090A0B0C}])
            data = u.dataout
            self.assertEqual(len(data), 24)
            # UNMAP DATA LENGTH = 22
            self.assertEqual(scsi_ba_to_int(data[0:2]), 22)
            # UNMAP BLOCK DESCRIPTOR DATA LENGTH = 16
            self.assertEqual(scsi_ba_to_int(data[2:4]), 16)
            # reserved bytes 4-7
            self.assertEqual(scsi_ba_to_int(data[4:8]), 0)
            # descriptor: LBA
            self.assertEqual(scsi_ba_to_int(data[8:16]), 0x0102030405060708)
            # descriptor: NUMBER OF LOGICAL BLOCKS
            self.assertEqual(scsi_ba_to_int(data[16:20]), 0x090A0B0C)
            # descriptor: reserved
            self.assertEqual(scsi_ba_to_int(data[20:24]), 0)

            # Two descriptors: verify lengths and both descriptors
            u = s.unmap(
                [{"lba": 0x100, "num_blocks": 0x10}, {"lba": 0x200, "num_blocks": 0x20}]
            )
            data = u.dataout
            self.assertEqual(len(data), 40)
            # UNMAP DATA LENGTH = 38
            self.assertEqual(scsi_ba_to_int(data[0:2]), 38)
            # UNMAP BLOCK DESCRIPTOR DATA LENGTH = 32
            self.assertEqual(scsi_ba_to_int(data[2:4]), 32)
            # descriptor 0
            self.assertEqual(scsi_ba_to_int(data[8:16]), 0x100)
            self.assertEqual(scsi_ba_to_int(data[16:20]), 0x10)
            # descriptor 1
            self.assertEqual(scsi_ba_to_int(data[24:32]), 0x200)
            self.assertEqual(scsi_ba_to_int(data[32:36]), 0x20)
