# coding: utf-8

# Copyright (C) 2024 by Folkert van Heusden <mail@vanheusden.com>
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_synchronizecache import SynchronizeCache
from pyscsi.pyscsi.scsi_enum_command import sbc
from tests.mock_device import MockDevice, MockSCSI


class CdbSynchronizeCacheTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(sbc)) as s:
            w = s.synchronizecache()
            cdb = w.cdb
            self.assertEqual(cdb[0], s.device.opcodes.SYNCHRONIZE_CACHE_10.value)
            self.assertEqual(cdb[1], 0)
            self.assertEqual(cdb[2], 0)
            self.assertEqual(cdb[3], 0)
            self.assertEqual(cdb[4], 0)
            self.assertEqual(cdb[5], 0)
            cdb = w.unmarshall_cdb(cdb)
            self.assertEqual(cdb["opcode"], s.device.opcodes.SYNCHRONIZE_CACHE_10.value)

            d = SynchronizeCache.unmarshall_cdb(SynchronizeCache.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
