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
