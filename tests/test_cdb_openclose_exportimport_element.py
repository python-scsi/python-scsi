# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_openclose_exportimport_element import (
    OpenCloseImportExportElement,
)
from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.utils.converter import scsi_ba_to_int

from .mock_device import MockDevice, MockSCSI


class CdbOpencloseExportimportElementTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(smc)) as s:
            m = s.opencloseimportexportelement(32, s.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT.serviceaction.CLOSE_IMPORTEXPORT_ELEMENT)
            cdb = m.cdb
            self.assertEqual(cdb[0], s.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT.value)
            self.assertEqual(scsi_ba_to_int(cdb[2:4]), 32)
            self.assertEqual(cdb[4], 0x01)
            cdb = m.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT.value)
            self.assertEqual(cdb['element_address'], 32)
            self.assertEqual(cdb['action_code'], s.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT.serviceaction.CLOSE_IMPORTEXPORT_ELEMENT)

            d = OpenCloseImportExportElement.unmarshall_cdb(OpenCloseImportExportElement.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
