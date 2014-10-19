#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.utils.converter import scsi_ba_to_int
from sgio.pyscsi.scsi_command import OPCODE, SERVICE_ACTION_IN

class MockReadCapacity16(object):
   def execute(self, cdb, dataout, datain, sense):
      pass

def main():
    s = SCSI(MockReadCapacity16())

    cdb = s.readcapacity16(alloclen=37)._cdb
    assert cdb[0] == OPCODE.SERVICE_ACTION_IN
    assert cdb[1] == SERVICE_ACTION_IN.READ_CAPACITY_16
    assert cdb[2:10] == bytearray(8)
    assert scsi_ba_to_int(cdb[10:14]) == 37
    assert cdb[14:16] == bytearray(2)

if __name__ == "__main__":
    main()

