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

from pyscsi.pyscsi.scsi_cdb_writesame10 import WriteSame10
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int

from .mock_device import MockDevice, MockSCSI


class CdbWritesame10Test(unittest.TestCase):
    def test_main(self):

        with MockSCSI(MockDevice(sbc)) as s:
            s.blocksize = 512

            data = bytearray(512)

            w = s.writesame10(1024, 27, data)
            cdb = w.cdb
            self.assertEqual(cdb[0], s.device.opcodes.WRITE_SAME_10.value)
            self.assertEqual(cdb[1], 0)
            self.assertEqual(scsi_ba_to_int(cdb[2:6]), 1024)
            self.assertEqual(cdb[6], 0)
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 27)
            self.assertEqual(cdb[9], 0)
            cdb = w.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.WRITE_SAME_10.value)
            self.assertEqual(cdb['wrprotect'], 0)
            self.assertEqual(cdb['anchor'], 0)
            self.assertEqual(cdb['unmap'], 0)
            self.assertEqual(cdb['lba'], 1024)
            self.assertEqual(cdb['group'], 0)
            self.assertEqual(cdb['nb'], 27)

            d = WriteSame10.unmarshall_cdb(WriteSame10.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

            w = s.writesame10(65536, 27, data, wrprotect=4, anchor=1, group=19)
            cdb = w.cdb
            self.assertEqual(cdb[0], s.device.opcodes.WRITE_SAME_10.value)
            self.assertEqual(cdb[1], 0x90)
            self.assertEqual(scsi_ba_to_int(cdb[2:6]), 65536)
            self.assertEqual(cdb[6], 0x13)
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 27)
            self.assertEqual(cdb[9], 0)
            cdb = w.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.WRITE_SAME_10.value)
            self.assertEqual(cdb['wrprotect'], 4)
            self.assertEqual(cdb['anchor'], 1)
            self.assertEqual(cdb['unmap'], 0)
            self.assertEqual(cdb['lba'], 65536)
            self.assertEqual(cdb['group'], 19)
            self.assertEqual(cdb['nb'], 27)

            d = WriteSame10.unmarshall_cdb(WriteSame10.marshall_cdb(cdb))
            self.assertEqual(d, cdb)

            w = s.writesame10(65536, 27, data, wrprotect=4, unmap=1)
            cdb = w.cdb
            self.assertEqual(cdb[0], s.device.opcodes.WRITE_SAME_10.value)
            self.assertEqual(cdb[1], 0x88)
            self.assertEqual(scsi_ba_to_int(cdb[2:6]), 65536)
            self.assertEqual(cdb[6], 0)
            self.assertEqual(scsi_ba_to_int(cdb[7:9]), 27)
            self.assertEqual(cdb[9], 0)
            cdb = w.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.WRITE_SAME_10.value)
            self.assertEqual(cdb['wrprotect'], 4)
            self.assertEqual(cdb['anchor'], 0)
            self.assertEqual(cdb['unmap'], 1)
            self.assertEqual(cdb['lba'], 65536)
            self.assertEqual(cdb['group'], 0)
            self.assertEqual(cdb['nb'], 27)

            d = WriteSame10.unmarshall_cdb(WriteSame10.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
