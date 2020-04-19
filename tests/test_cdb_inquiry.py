# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_inquiry import Inquiry
from pyscsi.pyscsi.scsi_enum_command import spc
from pyscsi.utils.converter import scsi_ba_to_int

from .mock_device import MockDevice, MockSCSI


class CdbInquiryTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(spc)) as s:
            # cdb for standard page request
            i = s.inquiry(alloclen=128)
            cdb = i.cdb
            self.assertEqual(cdb[0], s.device.opcodes.INQUIRY.value)
            self.assertEqual(cdb[1:3], bytearray(2))
            self.assertEqual(scsi_ba_to_int(cdb[3:5]), 128)
            self.assertEqual(cdb[5], 0)
            cdb = i.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.INQUIRY.value)
            self.assertEqual(cdb['evpd'], 0)
            self.assertEqual(cdb['page_code'], 0)
            self.assertEqual(cdb['alloc_len'], 128)

            d = Inquiry.unmarshall_cdb(Inquiry.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

            # supported vpd pages
            i = s.inquiry(evpd=1, page_code=0x88, alloclen=300)
            cdb = i.cdb
            self.assertEqual(cdb[0], s.device.opcodes.INQUIRY.value)
            self.assertEqual(cdb[1], 0x01)
            self.assertEqual(cdb[2], 0x88)
            self.assertEqual(scsi_ba_to_int(cdb[3:5]), 300)
            self.assertEqual(cdb[5], 0)
            cdb = i.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.INQUIRY.value)
            self.assertEqual(cdb['evpd'], 1)
            self.assertEqual(cdb['page_code'], 0x88)
            self.assertEqual(cdb['alloc_len'], 300)

            d = Inquiry.unmarshall_cdb(Inquiry.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
