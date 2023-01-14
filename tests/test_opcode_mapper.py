# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_enum_command import sbc, smc, spc, ssc


class OpcodeMapperTest(unittest.TestCase):
    def test_main(self):
        self.assertEqual(spc.SPC_OPCODE_A4.value, 0xA4)
        self.assertEqual(sbc.SBC_OPCODE_9E.value, 0x9E)
        self.assertEqual(ssc.READ_ELEMENT_STATUS_ATTACHED.value, 0xB4)
        self.assertEqual(smc.MAINTENANCE_IN.value, 0xA3)
        self.assertEqual(
            smc.MAINTENANCE_IN.serviceaction.REPORT_DEVICE_IDENTIFICATION, 0x07
        )
