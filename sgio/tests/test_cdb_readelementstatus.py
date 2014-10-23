#!/usr/bin/env python
# coding: utf-8

import sys

from sgio.pyscsi.scsi import SCSI
from sgio.utils.converter import scsi_ba_to_int
from sgio.pyscsi.scsi_command import OPCODE
from sgio.pyscsi import scsi_cdb_readelementstatus as READELEMENTSTATUS

class MockReadElementStatus(object):
   def execute(self, cdb, dataout, datain, sense):
      pass

def main():
    s = SCSI(MockReadElementStatus())

    # cdb for SMC: ReadElementStatus
    r = s.readelementstatus(300, 700, element_type=READELEMENTSTATUS.ELEMENT_TYPE.STORAGE, voltag=1, curdata=1, dvcid=1)
    cdb = r._cdb
    assert cdb[0] == OPCODE.READ_ELEMENT_STATUS
    assert cdb[1] == 0x10 | READELEMENTSTATUS.ELEMENT_TYPE.STORAGE
    assert scsi_ba_to_int(cdb[2:4]) == 300
    assert scsi_ba_to_int(cdb[4:6]) == 700
    assert cdb[6] == 0x03
    assert scsi_ba_to_int(cdb[7:10]) == 16384
    cdb = r.unmarshall_cdb(cdb)
    assert cdb['opcode'] == OPCODE.READ_ELEMENT_STATUS
    assert cdb['voltag'] == 1
    assert cdb['element_type'] == READELEMENTSTATUS.ELEMENT_TYPE.STORAGE
    assert cdb['starting_element_address'] == 300
    assert cdb['num_elements'] == 700
    assert cdb['curdata'] == 1
    assert cdb['dvcid'] == 1
    assert cdb['alloc_len'] == 16384

if __name__ == "__main__":
    main()

