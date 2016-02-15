#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_cdb_writesame16 import WriteSame16


class MockWriteSame16(object):
    def execute(self, cdb, dataout, datain, sense):
        pass


def main():
    dev = MockWriteSame16()
    dev.opcodes = sbc
    s = SCSI(dev)
    s.blocksize = 512
    data = bytearray(512)

    w = s.writesame16(1024, 27, data, ndob=True)
    cdb = w.cdb
    assert cdb[0] == s.device.opcodes.WRITE_SAME_16.value
    assert cdb[1] == 0
    assert scsi_ba_to_int(cdb[2:10]) == 1024
    assert scsi_ba_to_int(cdb[10:14]) == 27
    assert cdb[14] == 0
    assert cdb[15] == 0
    cdb = w.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.WRITE_SAME_16.value
    assert cdb['wrprotect'] == 0
    assert cdb['anchor'] == 0
    assert cdb['unmap'] == 0
    assert cdb['ndob'] == 0
    assert cdb['lba'] == 1024
    assert cdb['group'] == 0
    assert cdb['nb'] == 27

    d = WriteSame16.unmarshall_cdb(WriteSame16.marshall_cdb(cdb))
    assert d == cdb

    w = s.writesame16(65536, 27, data, wrprotect=4, anchor=1, group=19)
    cdb = w.cdb
    assert cdb[0] == s.device.opcodes.WRITE_SAME_16.value
    assert cdb[1] == 0x90
    assert scsi_ba_to_int(cdb[2:10]) == 65536
    assert scsi_ba_to_int(cdb[10:14]) == 27
    assert cdb[14] == 0x13
    assert cdb[15] == 0
    cdb = w.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.WRITE_SAME_16.value
    assert cdb['wrprotect'] == 4
    assert cdb['anchor'] == 1
    assert cdb['unmap'] == 0
    assert cdb['ndob'] == 0
    assert cdb['lba'] == 65536
    assert cdb['group'] == 19
    assert cdb['nb'] == 27

    d = WriteSame16.unmarshall_cdb(WriteSame16.marshall_cdb(cdb))
    assert d == cdb

    w = s.writesame16(65536, 27, data, wrprotect=4, unmap=1, ndob=1)
    cdb = w.cdb
    assert cdb[0] == s.device.opcodes.WRITE_SAME_16.value
    assert cdb[1] == 0x89
    assert scsi_ba_to_int(cdb[2:10]) == 65536
    assert scsi_ba_to_int(cdb[10:14]) == 27
    assert cdb[14] == 0
    assert cdb[15] == 0
    cdb = w.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.WRITE_SAME_16.value
    assert cdb['wrprotect'] == 4
    assert cdb['anchor'] == 0
    assert cdb['unmap'] == 1
    assert cdb['ndob'] == 1
    assert cdb['lba'] == 65536
    assert cdb['group'] == 0
    assert cdb['nb'] == 27

    d = WriteSame16.unmarshall_cdb(WriteSame16.marshall_cdb(cdb))
    assert d == cdb

if __name__ == "__main__":
    main()

