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

    r = s.readcapacity10()
    cdb = r._cdb
    assert cdb[0] == OPCODE.READ_CAPACITY_10
    assert cdb[1:10] == bytearray(9)
    cdb = r.unmarshall_cdb(cdb)
    assert cdb['opcode'] == OPCODE.READ_CAPACITY_10

if __name__ == "__main__":
    main()

