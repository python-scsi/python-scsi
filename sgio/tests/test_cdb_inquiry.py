#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.utils.converter import scsi_ba_to_int
from sgio.pyscsi.scsi_command import OPCODE

class MockInquiry(object):
   def execute(self, cdb, dataout, datain, sense):
      pass

def main():
    s = SCSI(MockInquiry())

    # cdb for standard page request
    cdb = s.inquiry(alloclen=128)._cdb
    assert cdb[0] == OPCODE.INQUIRY
    assert cdb[1:3] == bytearray(2)
    assert scsi_ba_to_int(cdb[3:5]) == 128
    assert cdb[5] == 0

    # supported vpd pages
    cdb = s.inquiry(evpd=1, page_code=0x88, alloclen=128)._cdb
    assert cdb[0] == OPCODE.INQUIRY
    assert cdb[1] == 0x01
    assert cdb[2] == 0x88
    assert scsi_ba_to_int(cdb[3:5]) == 128
    assert cdb[5] == 0

if __name__ == "__main__":
    main()

