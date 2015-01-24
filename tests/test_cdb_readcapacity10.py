#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.pyscsi.scsi_cdb_readcapacity10 import ReadCapacity10


class MockReadCapacity10(object):
    def execute(self, cdb, dataout, datain, sense):
        pass


def main():
    dev = MockReadCapacity10()
    dev.opcodes = sbc
    s = SCSI(dev)

    s.device.opcodes = sbc
    r = s.readcapacity10()
    cdb = r.cdb
    assert cdb[0] == s.device.opcodes.READ_CAPACITY_10.value
    assert cdb[1:10] == bytearray(9)
    cdb = r.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.READ_CAPACITY_10.value

    d = ReadCapacity10.unmarshall_cdb(ReadCapacity10.marshall_cdb(cdb))
    assert d == cdb

if __name__ == "__main__":
    main()

