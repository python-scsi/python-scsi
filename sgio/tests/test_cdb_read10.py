#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi.scsi_command import OPCODE
from sgio.utils.converter import scsi_ba_to_int

class MockRead10(object):
   def execute(self, cdb, dataout, datain, sense):
      pass

def main():
    s = SCSI(MockRead10())

    cdb = s.read10(1024, 27)._cdb
    assert cdb[0] == OPCODE.READ_10
    assert cdb[1] == 0
    assert scsi_ba_to_int(cdb[2:6]) == 1024
    assert cdb[6] == 0
    assert scsi_ba_to_int(cdb[7:9]) == 27
    assert cdb[9] == 0

    cdb = s.read10(1024, 27, rdprotect=2, dpo=1, fua=1, rarc=1, group=19)._cdb
    assert cdb[0] == OPCODE.READ_10
    assert cdb[1] == 0x5c
    assert scsi_ba_to_int(cdb[2:6]) == 1024
    assert cdb[6] == 0x13
    assert scsi_ba_to_int(cdb[7:9]) == 27
    assert cdb[9] == 0

if __name__ == "__main__":
    main()

