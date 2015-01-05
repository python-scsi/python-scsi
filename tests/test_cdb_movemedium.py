#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import OPCODE
from pyscsi.utils.converter import scsi_ba_to_int


class MockMoveMedium(object):
    def execute(self, cdb, dataout, datain, sense):
        pass


def main():
    s = SCSI(MockMoveMedium())

    m = s.movemedium(15, 32, 64, invert=1)
    cdb = m.cdb
    assert cdb[0] == OPCODE.MOVE_MEDIUM
    assert cdb[1] == 0
    assert scsi_ba_to_int(cdb[2:4]) == 15
    assert scsi_ba_to_int(cdb[4:6]) == 32
    assert scsi_ba_to_int(cdb[6:8]) == 64
    assert cdb[8] == 0
    assert cdb[9] == 0
    assert cdb[10] == 0x01
    cdb = m.unmarshall_cdb(cdb)
    assert cdb['opcode'] == OPCODE.MOVE_MEDIUM
    assert cdb['medium_transport_address'] == 15
    assert cdb['source_address'] == 32
    assert cdb['destination_address'] == 64
    assert cdb['invert'] == 1


if __name__ == "__main__":
    main()

