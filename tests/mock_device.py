# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
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

    def execute(self, cdb, dataout, datain, sense):
        pass

    def open(self):
        pass

    def close(self):
        pass
