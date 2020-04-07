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

from mock_device import MockDevice, MockSCSI
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.pyscsi.scsi_cdb_readcapacity16 import ReadCapacity16


class MockReadCapacity16(MockDevice):

    def execute(self, cmd):
        # lba
        cmd.datain[0:8] = [0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        # block size
        cmd.datain[8:12] = [0x00, 0x00, 0x10, 0x00]
        cmd.datain[12] = 0x09  # P_TYPE:4 PROT_EN:1
        cmd.datain[13] = 0x88  # P_I_EXPONENT:8 LBPPBE:8
        cmd.datain[14] = 0xe0  # LBPME:1 LBPRZ:1 LOWEST_ALIGNED_LBA:top-bit-set
        cmd.datain[15] = 0x01  # LOWEST_ALIGNED_LBA:bottom-bit-set


def main():
    with MockSCSI(MockReadCapacity16(sbc)) as s:
        i = s.readcapacity16().result
        assert i['returned_lba'] == 281474976710656
        assert i['block_length'] == 4096
        assert i['p_type'] == 4
        assert i['prot_en'] == 1
        assert i['p_i_exponent'] == 8
        assert i['lbppbe'] == 8
        assert i['lbpme'] == 1
        assert i['lbprz'] == 1
        assert i['lowest_aligned_lba'] == 8193

        d = ReadCapacity16.unmarshall_datain(ReadCapacity16.marshall_datain(i))
        assert d == i


if __name__ == "__main__":
    main()

