# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_readcapacity10 import ReadCapacity10
from pyscsi.pyscsi.scsi_enum_command import sbc

from .mock_device import MockDevice, MockSCSI


class MockReadCapacity10(MockDevice):

    def execute(self, cmd):
        # lba
        cmd.datain[0:4] = [0x00, 0x01, 0x00, 0x00]
        # block size
        cmd.datain[4:8] = [0x00, 0x00, 0x10, 0x00]

class UnmarshallReadcapacity10Test(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockReadCapacity10(sbc)) as s:
            i = s.readcapacity10().result
            self.assertEqual(i['returned_lba'], 65536)
            self.assertEqual(i['block_length'], 4096)

            d = ReadCapacity10.unmarshall_datain(ReadCapacity10.marshall_datain(i))
            self.assertEqual(d, i)
