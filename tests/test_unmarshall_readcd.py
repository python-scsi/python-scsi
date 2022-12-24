# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_readcd import ReadCd
from pyscsi.pyscsi.scsi_enum_command import mmc

from tests.mock_device import MockDevice, MockSCSI

_SYNC = bytes([0x00, 0xff, 0xff, 0xff, 0xff, 0xff,
               0xff, 0xff, 0xff, 0xff, 0xff, 0x00])

#
# Mock for a read of two sectors for SYNC and SubChannel type 2
#
class MockReadCD_SyncSubC(MockDevice):
    def execute(self, cmd, en_raw_sense: bool=False):
        # sync
        cmd.datain[0:12] = _SYNC
        # subchannel
        cmd.datain[12:28] = [0x41, 0x01, 0x01, 0x00,  0x08, 0x40, 0x00, 0x00,
                             0x10, 0x40, 0x19, 0xcd,  0x00, 0x00, 0x00, 0x00]

        # sync
        cmd.datain[28:40] = _SYNC
        # subchannel
        cmd.datain[40:56] = [0x41, 0x01, 0x01, 0x00,  0x08, 0x41, 0x00, 0x00,
                             0x10, 0x41, 0xa3, 0xbd,  0x00, 0x00, 0x00, 0x80]

#
# Mock for a read of two sectors for SYNC and SectorHeader
#
class MockReadCD_SyncSH(MockDevice):
    def execute(self, cmd, en_raw_sense: bool=False):
        # sync
        cmd.datain[0:12] = _SYNC
        # subchannel
        cmd.datain[12:16] = [0x00, 0x10, 0x40, 0x01]

        # sync
        cmd.datain[16:28] = _SYNC
        # subchannel
        cmd.datain[28:32] = [0x00, 0x10, 0x41, 0x01]

class UnmarshallReadCdTest(unittest.TestCase):
    def test_main(self):
        # SYNC and SubChannel
        with MockSCSI(MockReadCD_SyncSubC(mmc)) as s:
            i = s.readcd(lba=640, tl=2, est=2, mcsb=0x10, scsb=2, c2ei=0).result
            self.assertEqual(i[640]['sync'], _SYNC)
            self.assertEqual(i[640]['subchannel']['c'], 4)
            self.assertEqual(i[640]['subchannel']['adr'], 1)
            self.assertEqual(i[640]['subchannel']['track-number'], 1)
            self.assertEqual(i[640]['subchannel']['index-number'], 1)
            self.assertEqual(i[640]['subchannel']['min'], 0)
            self.assertEqual(i[640]['subchannel']['sec'], 8)
            self.assertEqual(i[640]['subchannel']['frame'], 64)
            self.assertEqual(i[640]['subchannel']['zero'], 0)
            self.assertEqual(i[640]['subchannel']['amin'], 0)
            self.assertEqual(i[640]['subchannel']['asec'], 16)
            self.assertEqual(i[640]['subchannel']['aframe'], 64)
            self.assertEqual(i[640]['subchannel']['crc'], 6605)
            self.assertEqual(i[640]['subchannel']['p'], 0)

            self.assertEqual(i[641]['sync'], _SYNC)
            self.assertEqual(i[641]['subchannel']['c'], 4)
            self.assertEqual(i[641]['subchannel']['adr'], 1)
            self.assertEqual(i[641]['subchannel']['track-number'], 1)
            self.assertEqual(i[641]['subchannel']['index-number'], 1)
            self.assertEqual(i[641]['subchannel']['min'], 0)
            self.assertEqual(i[641]['subchannel']['sec'], 8)
            self.assertEqual(i[641]['subchannel']['frame'], 65)
            self.assertEqual(i[641]['subchannel']['zero'], 0)
            self.assertEqual(i[641]['subchannel']['amin'], 0)
            self.assertEqual(i[641]['subchannel']['asec'], 16)
            self.assertEqual(i[641]['subchannel']['aframe'], 65)
            self.assertEqual(i[641]['subchannel']['crc'], 41917)
            self.assertEqual(i[641]['subchannel']['p'], 1)

        # SYNC and SectorHeader
        with MockSCSI(MockReadCD_SyncSH(mmc)) as s:
            i = s.readcd(lba=640, tl=2, est=2, mcsb=0x14, scsb=0, c2ei=0).result
            self.assertEqual(i[640]['sync'], _SYNC)
            self.assertEqual(i[640]['sector-header']['minute'], 0)
            self.assertEqual(i[640]['sector-header']['second'], 16)
            self.assertEqual(i[640]['sector-header']['frame'], 64)
            self.assertEqual(i[640]['sector-header']['mode'], 1)

            self.assertEqual(i[641]['sync'], _SYNC)
            self.assertEqual(i[641]['sector-header']['minute'], 0)
            self.assertEqual(i[641]['sector-header']['second'], 16)
            self.assertEqual(i[641]['sector-header']['frame'], 65)
            self.assertEqual(i[641]['sector-header']['mode'], 1)
