#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi import scsi_cdb_inquiry as INQUIRY

class MockInquiryStandard(object):
   def execute(self, cdb, dataout, datain, sense):
       datain[0] = 0x25 # QUAL:1 TYPE:5
       datain[1] = 0x80 # RMB:1
       datain[2] = 0x07 # VERSION:7
       datain[3] = 0x23 # NORMACA:1 HISUP:0 RDF:3
       datain[4] = 0x40 # ADDITIONAL LENGTH:64
       datain[5] = 0xb9 # SCCS:1 ACC:0 TGPS:3 3PC:1 PROTECT:1
       datain[6] = 0x71 # ENCSERV:1 VS:1 MULTIP:1 ADDR16:1
       datain[7] = 0x33 # WBUS16:1 SYNC:1 CMDQUE:1 VS2:1
       # t10 vendor id
       datain[8:16] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
       # product id
       datain[16:32] = ['i', 'i','i', 'i','i', 'i','i', 'i',
                        'j', 'j','j', 'j','j', 'j','j', 'j']
       # product revision level
       datain[32:36] = ['r', 'e', 'v', 'n']
       datain[56] = 0x09 # CLOCKING:2 QAS:0 IUS:1

class MockLBP(object):
   def execute(self, cdb, dataout, datain, sense):
       datain[0] = 0x00 # QUAL:0 TYPE:0
       datain[1] = 0xb2 # logical block provisioning
       datain[2] = 0x00 #
       datain[3] = 0x04 # page length == 4
       datain[4] = 0x12 # threshold exponent
       datain[5] = 0xe7 # LBPU:1 LBPWS:1 LBPWS10:1 LBPRZ:1 ANC_SUP:1 DP:1
       datain[6] = 0x02 # Provisioning Type:2
       datain[7] = 0x00 # 

class MockUSN(object):
   def execute(self, cdb, dataout, datain, sense):
       datain[0] = 0x00 # QUAL:0 TYPE:0
       datain[1] = 0xb2 # logical block provisioning
       datain[2] = 0x00 #
       datain[3] = 0x04 # page length == 4
       datain[4:8] = "ABCD"

def main():
    s = SCSI(MockInquiryStandard())
    i = s.inquiry().result
    assert i['peripheral_qualifier'] == 1
    assert i['peripheral_device_type'] == 5
    assert i['rmb'] == 1
    assert i['version'] == 7
    assert i['normaca'] == 1
    assert i['hisup'] == 0
    assert i['response_data_format'] == 3
    assert i['additional_length'] == 64
    assert i['sccs'] == 1
    assert i['acc'] == 0
    assert i['tpgs'] == 3
    assert i['3pc'] == 1
    assert i['protect'] == 1
    assert i['encserv'] == 1
    assert i['vs'] == 1
    assert i['multip'] == 1
    assert i['addr16'] == 1
    assert i['wbus16'] == 1
    assert i['sync'] == 1
    assert i['cmdque'] == 1
    assert i['vs2'] == 1
    assert i['clocking'] == 2 
    assert i['qas'] == 0
    assert i['ius'] == 1
    assert i['t10_vendor_identification'] == 'abcdefgh'
    assert i['product_identification'] == 'iiiiiiiijjjjjjjj'
    assert i['product_revision_level'] == 'revn'

    s = SCSI(MockLBP())
    i = s.inquiry(evpd=1, page_code=INQUIRY.VPD.LOGICAL_BLOCK_PROVISIONING).result
    assert i['peripheral_qualifier'] == 0
    assert i['peripheral_qualifier'] == 0
    assert i['threshold_exponent'] == 0x12
    assert i['lbpu'] == 1
    assert i['lpbws'] == 1
    assert i['lbpws10'] == 1
    assert i['lbprz'] == 1
    assert i['anc_sup'] == 1
    assert i['dp'] == 1
    assert i['provisioning_type'] == INQUIRY.PROVISIONING_TYPE.THIN_PROVISIONED

    s = SCSI(MockUSN())
    i = s.inquiry(evpd=1, page_code=INQUIRY.VPD.UNIT_SERIAL_NUMBER).result
    assert i['peripheral_qualifier'] == 0
    assert i['peripheral_qualifier'] == 0
    assert i['unit_serial_number'] == "ABCD"

if __name__ == "__main__":
    main()

