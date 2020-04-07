#!/usr/bin/env python
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

from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_cdb_write10 import Write10
from mock_device import MockDevice, MockSCSI

class CdbWrite10Test(unittest.TestCase):
    def test_main(self):

        with MockSCSI(MockDevice(sbc)) as s:
            s.blocksize = 512

            data = bytearray(27 * 512)

            w = s.write10(1024, 27, data)
            cdb = w.cdb
            assert cdb[0] == s.device.opcodes.WRITE_10.value
            assert cdb[1] == 0
            assert scsi_ba_to_int(cdb[2:6]) == 1024
            assert cdb[6] == 0
            assert scsi_ba_to_int(cdb[7:9]) == 27
            assert cdb[9] == 0
            cdb = w.unmarshall_cdb(cdb)
            assert cdb['opcode'] == s.device.opcodes.WRITE_10.value
            assert cdb['wrprotect'] == 0
            assert cdb['dpo'] == 0
            assert cdb['fua'] == 0
            assert cdb['lba'] == 1024
            assert cdb['group'] == 0
            assert cdb['tl'] == 27

            d = Write10.unmarshall_cdb(Write10.marshall_cdb(cdb))
            assert d == cdb

            w = s.write10(65536, 27, data, wrprotect=2, dpo=1, fua=1, group=19)
            cdb = w.cdb
            assert cdb[0] == s.device.opcodes.WRITE_10.value
            assert cdb[1] == 0x58
            assert scsi_ba_to_int(cdb[2:6]) == 65536
            assert cdb[6] == 0x13
            assert scsi_ba_to_int(cdb[7:9]) == 27
            assert cdb[9] == 0
            cdb = w.unmarshall_cdb(cdb)
            assert cdb['opcode'] == s.device.opcodes.WRITE_10.value
            assert cdb['wrprotect'] == 2
            assert cdb['dpo'] == 1
            assert cdb['fua'] == 1
            assert cdb['lba'] == 65536
            assert cdb['group'] == 19
            assert cdb['tl'] == 27

            d = Write10.unmarshall_cdb(Write10.marshall_cdb(cdb))
            assert d == cdb

if __name__ == '__main__':
    unittest.main()
