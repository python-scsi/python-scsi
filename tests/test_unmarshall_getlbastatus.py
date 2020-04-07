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

from pyscsi.utils.converter import scsi_int_to_ba
from pyscsi.pyscsi.scsi_enum_getlbastatus import P_STATUS
from pyscsi.pyscsi.scsi_enum_command import sbc
from mock_device import MockDevice, MockSCSI
from pyscsi.pyscsi.scsi_cdb_getlbastatus import GetLBAStatus


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


def main():
    with MockSCSI(MockGetLBAStatus(sbc)) as s:
        i = s.getlbastatus(0).result
        assert len(i['lbas']) == 2
        assert i['lbas'][0]['lba'] == 1023
        assert i['lbas'][0]['num_blocks'] == 27
        assert i['lbas'][0]['p_status'] == P_STATUS.MAPPED
        assert i['lbas'][1]['lba'] == 200000
        assert i['lbas'][1]['num_blocks'] == 9999
        assert i['lbas'][1]['p_status'] == P_STATUS.DEALLOCATED

        d = GetLBAStatus.unmarshall_datain(GetLBAStatus.marshall_datain(i))
        assert d == i


if __name__ == "__main__":
    main()

