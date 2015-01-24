#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_cdb_readcapacity10 import ReadCapacity10


class MockReadCapacity10(object):
    def execute(self, cdb, dataout, datain, sense):
        # lba
        datain[0:4] = [0x00, 0x01, 0x00, 0x00]
        # block size
        datain[4:8] = [0x00, 0x00, 0x10, 0x00]


def main():
    s = SCSI(MockReadCapacity10())

    i = s.readcapacity10().result
    assert i['returned_lba'] == 65536
    assert i['block_length'] == 4096

    d = ReadCapacity10.unmarshall_datain(ReadCapacity10.marshall_datain(i))
    assert d == i

if __name__ == "__main__":
    main()

