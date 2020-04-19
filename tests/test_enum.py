# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.utils.enum import Enum

enum_dict = {'A': 1,
             'B': 2,
             'C': 3, }

class EnumTest(unittest.TestCase):
    def test_main(self):
        i = Enum(enum_dict)
        self.assertEqual(i.A, 1)
        self.assertEqual(i.B, 2)
        self.assertEqual(i.C, 3)
        self.assertEqual(i[1], 'A')
        self.assertEqual(i[2], 'B')
        self.assertEqual(i[3], 'C')
        self.assertEqual(i[4], '')
        a = Enum(A=1, B=2, C=3)
        self.assertEqual(a.A, 1)
        self.assertEqual(a.B, 2)
        self.assertEqual(a.C, 3)
        self.assertEqual(a[1], 'A')
        self.assertEqual(a[2], 'B')
        self.assertEqual(a[3], 'C')
        self.assertEqual(a[4], '')
        self.assertEqual(smc.WRITE_BUFFER.value, 0x3b)
        self.assertEqual(smc.WRITE_BUFFER.name, 'WRITE_BUFFER')
