# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi import SCSI


class MockSCSI(SCSI):

    def __init__(self, dev):
        self.device = dev
        pass


class MockDevice(object):
    _opcodes = None

    def __init__(self, opcodes):
        self.opcodes = opcodes

    @property
    def opcodes(self):
        return self._opcodes

    @opcodes.setter
    def opcodes(self, value):
        self._opcodes = value

    def execute(self, cmd):
        pass

    def open(self):
        pass

    def close(self):
        pass
