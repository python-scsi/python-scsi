# coding: utf-8
# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import unittest

from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_enum_command import spc
from pyscsi.pyscsi.scsi_cdb_report_priority import ReportPriority
from .mock_device import MockDevice, MockSCSI

class CdbReportpriorityTest(unittest.TestCase):
    def test_main(self):

        with MockSCSI(MockDevice(spc)) as s:
            r = s.reportpriority(priority=0x00, alloclen=1112527)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.SPC_OPCODE_A3.value)
            self.assertEqual(cdb[1], s.device.opcodes.SPC_OPCODE_A3.serviceaction.REPORT_PRIORITY)
            self.assertEqual(cdb[2], 0)
            self.assertEqual(scsi_ba_to_int(cdb[6:10]), 1112527)
            self.assertEqual(cdb[10:12], bytearray(2))
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.SPC_OPCODE_A3.value)
            self.assertEqual(cdb['service_action'], s.device.opcodes.SPC_OPCODE_A3.serviceaction.REPORT_PRIORITY)
            self.assertEqual(cdb['priority_reported'], 0)
            self.assertEqual(cdb['alloc_len'], 1112527)

            d = ReportPriority.unmarshall_cdb(ReportPriority.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
