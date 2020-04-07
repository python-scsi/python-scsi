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

from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_enum_command import spc
from pyscsi.pyscsi.scsi_cdb_report_priority import ReportPriority
from mock_device import MockDevice, MockSCSI


def main():

    with MockSCSI(MockDevice(spc)) as s:
        r = s.reportpriority(priority=0x00, alloclen=1112527)
        cdb = r.cdb
        assert cdb[0] == s.device.opcodes.SPC_OPCODE_A3.value
        assert cdb[1] == s.device.opcodes.SPC_OPCODE_A3.serviceaction.REPORT_PRIORITY
        assert cdb[2] == 0
        assert scsi_ba_to_int(cdb[6:10]) == 1112527
        assert cdb[10:12] == bytearray(2)
        cdb = r.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.SPC_OPCODE_A3.value
        assert cdb['service_action'] == s.device.opcodes.SPC_OPCODE_A3.serviceaction.REPORT_PRIORITY
        assert cdb['priority_reported'] == 0
        assert cdb['alloc_len'] == 1112527

        d = ReportPriority.unmarshall_cdb(ReportPriority.marshall_cdb(cdb))
        assert d == cdb


if __name__ == "__main__":
    main()