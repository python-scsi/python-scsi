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


class CdbReadcapacity10Test(unittest.TestCase):
    def test_main(self):

        with MockSCSI(MockDevice(sbc)) as s:
            r = s.readcapacity10()
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.READ_CAPACITY_10.value)
            self.assertEqual(cdb[1:10], bytearray(9))
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.READ_CAPACITY_10.value)

            d = ReadCapacity10.unmarshall_cdb(ReadCapacity10.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
