#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_cdb_read10 import Read10


class MockRead10(object):
    def execute(self, cdb, dataout, datain, sense):
        pass


def main():
    dev = MockRead10()
    dev.opcodes = sbc
    s = SCSI(dev)

    r = s.read10(1024, 27)
    cdb = r.cdb
    assert cdb[0] == s.device.opcodes.READ_10.value
    assert cdb[1] == 0
    assert scsi_ba_to_int(cdb[2:6]) == 1024
    assert cdb[6] == 0
    assert scsi_ba_to_int(cdb[7:9]) == 27
    assert cdb[9] == 0
    cdb = r.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.READ_10.value
    assert cdb['rdprotect'] == 0
    assert cdb['dpo'] == 0
    assert cdb['fua'] == 0
    assert cdb['rarc'] == 0
    assert cdb['lba'] == 1024
    assert cdb['group'] == 0
    assert cdb['tl'] == 27

    d = Read10.unmarshall_cdb(Read10.marshall_cdb(cdb))
    assert d == cdb

    r = s.read10(1024, 27, rdprotect=2, dpo=1, fua=1, rarc=1, group=19)
    cdb = r.cdb
    assert cdb[0] == s.device.opcodes.READ_10.value
    assert cdb[1] == 0x5c
    assert scsi_ba_to_int(cdb[2:6]) == 1024
    assert cdb[6] == 0x13
    assert scsi_ba_to_int(cdb[7:9]) == 27
    assert cdb[9] == 0
    cdb = r.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.READ_10.value
    assert cdb['rdprotect'] == 2
    assert cdb['dpo'] == 1
    assert cdb['fua'] == 1
    assert cdb['rarc'] == 1
    assert cdb['lba'] == 1024
    assert cdb['group'] == 19
    assert cdb['tl'] == 27

    d = Read10.unmarshall_cdb(Read10.marshall_cdb(cdb))
    assert d == cdb

if __name__ == "__main__":
    main()

