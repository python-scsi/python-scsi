#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi import scsi_cdb_inquiry as INQUIRY

class MockInquiryStandard(object):
   def execute(self, cdb, dataout, datain, sense):
       datain[0] = 0x25
       datain[1] = 0x80

def main():
    sd = MockInquiryStandard()
    s = SCSI(sd)

    i = s.inquiry().result
    assert i['peripheral_qualifier'] == 0x01
    assert i['peripheral_device_type'] == 0x05

if __name__ == "__main__":
    main()

