# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_initelementstatus import InitializeElementStatus
from pyscsi.pyscsi.scsi_enum_command import smc

from .mock_device import MockDevice, MockSCSI


class CdbInitelementstatusTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockDevice(smc)) as s:
            r = s.initializeelementstatus()
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.INITIALIZE_ELEMENT_STATUS.value)
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(cdb['opcode'], s.device.opcodes.INITIALIZE_ELEMENT_STATUS.value)

            d = InitializeElementStatus.unmarshall_cdb(InitializeElementStatus.marshall_cdb(cdb))
            self.assertEqual(d, cdb)
