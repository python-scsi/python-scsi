# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_getlbastatus import GetLBAStatus
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.pyscsi.scsi_enum_getlbastatus import P_STATUS
from pyscsi.utils.converter import scsi_int_to_ba

from .mock_device import MockDevice, MockSCSI


class MockGetLBAStatus(MockDevice):

    def execute(self, cmd):
        cmd.datain[0:8] = bytearray(8)
        pos = 8

        lbas = bytearray(16)
        lbas[0:8] = scsi_int_to_ba(1023, 8)
        lbas[8:12] = scsi_int_to_ba(27, 4)
        lbas[12] = 0
        cmd.datain[pos:pos + len(lbas)] = lbas
        pos += len(lbas)

        lbas = bytearray(16)
        lbas[0:8] = scsi_int_to_ba(200000, 8)
        lbas[8:12] = scsi_int_to_ba(9999, 4)
        lbas[12] = 1
        cmd.datain[pos:pos + len(lbas)] = lbas
        pos += len(lbas)

        cmd.datain[0:4] = scsi_int_to_ba(pos - 4, 4)

class UnmarshallGetlbastatusTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockGetLBAStatus(sbc)) as s:
            i = s.getlbastatus(0).result
            self.assertEqual(len(i['lbas']), 2)
            self.assertEqual(i['lbas'][0]['lba'], 1023)
            self.assertEqual(i['lbas'][0]['num_blocks'], 27)
            self.assertEqual(i['lbas'][0]['p_status'], P_STATUS.MAPPED)
            self.assertEqual(i['lbas'][1]['lba'], 200000)
            self.assertEqual(i['lbas'][1]['num_blocks'], 9999)
            self.assertEqual(i['lbas'][1]['p_status'], P_STATUS.DEALLOCATED)

            d = GetLBAStatus.unmarshall_datain(GetLBAStatus.marshall_datain(i))
            self.assertEqual(d, i)
