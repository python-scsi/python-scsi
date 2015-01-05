#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_enum_command import OPCODE, SERVICE_ACTION_IN


class MockGetLBAStatus(object):
    def execute(self, cdb, dataout, datain, sense):
        pass


def main():
    s = SCSI(MockGetLBAStatus())

    r = s.getlbastatus(19938722, alloclen=1112527)
    cdb = r.cdb
    assert cdb[0] == OPCODE.SERVICE_ACTION_IN
    assert cdb[1] == SERVICE_ACTION_IN.GET_LBA_STATUS
    assert scsi_ba_to_int(cdb[2:10]) == 19938722
    assert scsi_ba_to_int(cdb[10:14]) == 1112527
    assert cdb[14:16] == bytearray(2)
    cdb = r.unmarshall_cdb(cdb)
    assert cdb['opcode'] == OPCODE.SERVICE_ACTION_IN
    assert cdb['service_action'] == SERVICE_ACTION_IN.GET_LBA_STATUS
    assert cdb['lba'] == 19938722
    assert cdb['alloc_len'] == 1112527

if __name__ == "__main__":
    main()

