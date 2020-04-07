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

from pyscsi.pyscsi.scsi_enum_command import smc
from mock_device import MockDevice, MockSCSI
from pyscsi.pyscsi.scsi_cdb_initelementstatus import InitializeElementStatus


def main():
    with MockSCSI(MockDevice(smc)) as s:
        r = s.initializeelementstatus()
        cdb = r.cdb
        assert cdb[0] == s.device.opcodes.INITIALIZE_ELEMENT_STATUS.value
        cdb = r.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.INITIALIZE_ELEMENT_STATUS.value

        d = InitializeElementStatus.unmarshall_cdb(InitializeElementStatus.marshall_cdb(cdb))
        assert d == cdb


if __name__ == "__main__":
    main()



