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

from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.utils.converter import scsi_ba_to_int
from mock_device import MockDevice, MockSCSI
from pyscsi.pyscsi.scsi_cdb_openclose_exportimport_element import OpenCloseImportExportElement

class CdbOpencloseExportimportElementTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(smc)) as s:
            m = s.opencloseimportexportelement(32, s.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT.serviceaction.CLOSE_IMPORTEXPORT_ELEMENT)
            cdb = m.cdb
            assert cdb[0] == s.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT.value
            assert scsi_ba_to_int(cdb[2:4]) == 32
            assert cdb[4] == 0x01
            cdb = m.unmarshall_cdb(cdb)
            assert cdb['opcode'] == s.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT.value
            assert cdb['element_address'] == 32
            assert cdb['action_code'] == s.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT.serviceaction.CLOSE_IMPORTEXPORT_ELEMENT

            d = OpenCloseImportExportElement.unmarshall_cdb(OpenCloseImportExportElement.marshall_cdb(cdb))
            assert d == cdb

if __name__ == '__main__':
    unittest.main()
