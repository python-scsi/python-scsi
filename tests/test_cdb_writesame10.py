#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import OPCODE
from pyscsi.utils.converter import scsi_ba_to_int


class MockWriteSame10(object):
    def execute(self, cdb, dataout, datain, sense):
        pass


def main():
    s = SCSI(MockWriteSame10())
    data = bytearray(512)

    w = s.writesame10(1024, 27, data)
    cdb = w.cdb
    assert cdb[0] == OPCODE.WRITE_SAME_10
    assert cdb[1] == 0
    assert scsi_ba_to_int(cdb[2:6]) == 1024
    assert cdb[6] == 0
    assert scsi_ba_to_int(cdb[7:9]) == 27
    assert cdb[9] == 0
    cdb = w.unmarshall_cdb(cdb)
    assert cdb['opcode'] == OPCODE.WRITE_SAME_10
    assert cdb['wrprotect'] == 0
    assert cdb['anchor'] == 0
    assert cdb['unmap'] == 0
    assert cdb['lba'] == 1024
    assert cdb['group'] == 0
    assert cdb['nb'] == 27

    w = s.writesame10(65536, 27, data, wrprotect=4, anchor=1, group=19)
    cdb = w.cdb
    assert cdb[0] == OPCODE.WRITE_SAME_10
    assert cdb[1] == 0x90
    assert scsi_ba_to_int(cdb[2:6]) == 65536
    assert cdb[6] == 0x13
    assert scsi_ba_to_int(cdb[7:9]) == 27
    assert cdb[9] == 0
    cdb = w.unmarshall_cdb(cdb)
    assert cdb['opcode'] == OPCODE.WRITE_SAME_10
    assert cdb['wrprotect'] == 4
    assert cdb['anchor'] == 1
    assert cdb['unmap'] == 0
    assert cdb['lba'] == 65536
    assert cdb['group'] == 19
    assert cdb['nb'] == 27

    w = s.writesame10(65536, 27, data, wrprotect=4, unmap=1)
    cdb = w.cdb
    assert cdb[0] == OPCODE.WRITE_SAME_10
    assert cdb[1] == 0x88
    assert scsi_ba_to_int(cdb[2:6]) == 65536
    assert cdb[6] == 0
    assert scsi_ba_to_int(cdb[7:9]) == 27
    assert cdb[9] == 0
    cdb = w.unmarshall_cdb(cdb)
    assert cdb['opcode'] == OPCODE.WRITE_SAME_10
    assert cdb['wrprotect'] == 4
    assert cdb['anchor'] == 0
    assert cdb['unmap'] == 1
    assert cdb['lba'] == 65536
    assert cdb['group'] == 0
    assert cdb['nb'] == 27

if __name__ == "__main__":
    main()

