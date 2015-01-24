#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import OPCODE
from pyscsi.pyscsi.scsi_cdb_readcapacity10 import ReadCapacity10


class MockReadCapacity10(object):
    def execute(self, cdb, dataout, datain, sense):
        pass


def main():
    s = SCSI(MockReadCapacity10())

    r = s.readcapacity10()
    cdb = r.cdb
    assert cdb[0] == OPCODE.READ_CAPACITY_10
    assert cdb[1:10] == bytearray(9)
    cdb = r.unmarshall_cdb(cdb)
    assert cdb['opcode'] == OPCODE.READ_CAPACITY_10

    d = ReadCapacity10.unmarshall_cdb(ReadCapacity10.marshall_cdb(cdb))
    assert d == cdb

if __name__ == "__main__":
    main()

