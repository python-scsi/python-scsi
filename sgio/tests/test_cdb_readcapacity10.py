#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi.scsi_command import OPCODE

class MockReadCapacity10(object):
   def execute(self, cdb, dataout, datain, sense):
      pass

def main():
    s = SCSI(MockReadCapacity10())

    cdb = s.readcapacity10()._cdb
    assert cdb[0] == OPCODE.READ_CAPACITY_10
    assert cdb[1:10] == bytearray(9)

if __name__ == "__main__":
    main()

