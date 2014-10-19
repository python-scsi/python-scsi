#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi.scsi_command import OPCODE
from sgio.utils.converter import scsi_ba_to_int

class MockWrite12(object):
   def execute(self, cdb, dataout, datain, sense):
      pass

def main():
    s = SCSI(MockWrite12())
    data = bytearray(27 * 512)

    cdb = s.write12(1024, 27, data)._cdb
    assert cdb[0] == OPCODE.WRITE_12
    assert cdb[1] == 0
    assert scsi_ba_to_int(cdb[2:6]) == 1024
    assert scsi_ba_to_int(cdb[6:10]) == 27
    assert cdb[10] == 0
    assert cdb[11] == 0

    cdb = s.write12(65536, 27, data, wrprotect=2, dpo=1, fua=1, group=19)._cdb
    assert cdb[0] == OPCODE.WRITE_12
    assert cdb[1] == 0x58
    assert scsi_ba_to_int(cdb[2:6]) == 65536
    assert scsi_ba_to_int(cdb[6:10]) == 27
    assert cdb[10] == 0x13
    assert cdb[11] == 0

if __name__ == "__main__":
    main()

