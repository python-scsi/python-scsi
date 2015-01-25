#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_cdb_writesame10 import WriteSame10


class MockWriteSame10(object):
    def execute(self, cdb, dataout, datain, sense):
        pass


def main():
    dev = MockWriteSame10()
    dev.opcodes = sbc
    s = SCSI(dev)

    data = bytearray(512)

    w = s.writesame10(1024, 27, data)
    cdb = w.cdb
    assert cdb[0] == s.device.opcodes.WRITE_SAME_10.value
    assert cdb[1] == 0
    assert scsi_ba_to_int(cdb[2:6]) == 1024
    assert cdb[6] == 0
    assert scsi_ba_to_int(cdb[7:9]) == 27
    assert cdb[9] == 0
    cdb = w.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.WRITE_SAME_10.value
    assert cdb['wrprotect'] == 0
    assert cdb['anchor'] == 0
    assert cdb['unmap'] == 0
    assert cdb['lba'] == 1024
    assert cdb['group'] == 0
    assert cdb['nb'] == 27

    d = WriteSame10.unmarshall_cdb(WriteSame10.marshall_cdb(cdb))
    assert d == cdb

    w = s.writesame10(65536, 27, data, wrprotect=4, anchor=1, group=19)
    cdb = w.cdb
    assert cdb[0] == s.device.opcodes.WRITE_SAME_10.value
    assert cdb[1] == 0x90
    assert scsi_ba_to_int(cdb[2:6]) == 65536
    assert cdb[6] == 0x13
    assert scsi_ba_to_int(cdb[7:9]) == 27
    assert cdb[9] == 0
    cdb = w.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.WRITE_SAME_10.value
    assert cdb['wrprotect'] == 4
    assert cdb['anchor'] == 1
    assert cdb['unmap'] == 0
    assert cdb['lba'] == 65536
    assert cdb['group'] == 19
    assert cdb['nb'] == 27

    d = WriteSame10.unmarshall_cdb(WriteSame10.marshall_cdb(cdb))
    assert d == cdb

    w = s.writesame10(65536, 27, data, wrprotect=4, unmap=1)
    cdb = w.cdb
    assert cdb[0] == s.device.opcodes.WRITE_SAME_10.value
    assert cdb[1] == 0x88
    assert scsi_ba_to_int(cdb[2:6]) == 65536
    assert cdb[6] == 0
    assert scsi_ba_to_int(cdb[7:9]) == 27
    assert cdb[9] == 0
    cdb = w.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.WRITE_SAME_10.value
    assert cdb['wrprotect'] == 4
    assert cdb['anchor'] == 0
    assert cdb['unmap'] == 1
    assert cdb['lba'] == 65536
    assert cdb['group'] == 0
    assert cdb['nb'] == 27

    d = WriteSame10.unmarshall_cdb(WriteSame10.marshall_cdb(cdb))
    assert d == cdb

if __name__ == "__main__":
    main()

