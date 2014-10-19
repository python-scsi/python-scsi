#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.utils.converter import scsi_ba_to_int
from sgio.pyscsi.scsi_command import OPCODE
from sgio.pyscsi import scsi_cdb_modesense6 as MODESENSE6

class MockModeSense6(object):
   def execute(self, cdb, dataout, datain, sense):
      pass

def main():
    s = SCSI(MockModeSense6())

    # cdb for SMC: ElementAddressAssignment
    cdb = s.modesense6(page_code=MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT)._cdb
    assert cdb[0] == OPCODE.MODE_SENSE_6
    assert cdb[1] == 0
    assert cdb[2] == MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT
    assert cdb[3] == 0
    assert cdb[4] == 96
    assert cdb[5] == 0

    cdb = s.modesense6(page_code=0, sub_page_code=3, dbd=1, pc=MODESENSE6.PC.DEFAULT, alloclen=90)._cdb
    assert cdb[0] == OPCODE.MODE_SENSE_6
    assert cdb[1] == 0x08
    assert cdb[2] == MODESENSE6.PC.DEFAULT << 6
    assert cdb[3] == 3
    assert cdb[4] == 90
    assert cdb[5] == 0
if __name__ == "__main__":
    main()

