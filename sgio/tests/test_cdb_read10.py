#!/usr/bin/env python
# coding: utf-8

from sgio.pyscsi.scsi import SCSI
from sgio.pyscsi.scsi_enum_command import OPCODE
from sgio.utils.converter import scsi_ba_to_int


class MockRead10(object):
    def execute(self, cdb, dataout, datain, sense):
        pass


def main():
    s = SCSI(MockRead10())

    r = s.read10(1024, 27)
    cdb = r.cdb
    assert cdb[0] == OPCODE.READ_10
    assert cdb[1] == 0
    assert scsi_ba_to_int(cdb[2:6]) == 1024
    assert cdb[6] == 0
    assert scsi_ba_to_int(cdb[7:9]) == 27
    assert cdb[9] == 0
    cdb = r.unmarshall_cdb(cdb)
    assert cdb['opcode'] == OPCODE.READ_10
    assert cdb['rdprotect'] == 0
    assert cdb['dpo'] == 0
    assert cdb['fua'] == 0
    assert cdb['rarc'] == 0
    assert cdb['lba'] == 1024
    assert cdb['group'] == 0
    assert cdb['tl'] == 27

    r = s.read10(1024, 27, rdprotect=2, dpo=1, fua=1, rarc=1, group=19)
    cdb = r.cdb
    assert cdb[0] == OPCODE.READ_10
    assert cdb[1] == 0x5c
    assert scsi_ba_to_int(cdb[2:6]) == 1024
    assert cdb[6] == 0x13
    assert scsi_ba_to_int(cdb[7:9]) == 27
    assert cdb[9] == 0
    cdb = r.unmarshall_cdb(cdb)
    assert cdb['opcode'] == OPCODE.READ_10
    assert cdb['rdprotect'] == 2
    assert cdb['dpo'] == 1
    assert cdb['fua'] == 1
    assert cdb['rarc'] == 1
    assert cdb['lba'] == 1024
    assert cdb['group'] == 19
    assert cdb['tl'] == 27

if __name__ == "__main__":
    main()

