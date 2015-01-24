#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_enum_command import sbc


class MockReadCapacity16(object):
    def execute(self, cdb, dataout, datain, sense):
        pass


def main():
    dev = MockReadCapacity16()
    dev.opcodes = sbc
    s = SCSI(dev)

    r = s.readcapacity16(alloclen=37)
    cdb = r.cdb
    assert cdb[0] == s.device.opcodes.SBC_OPCODE_9E.value
    assert cdb[1] == s.device.opcodes.SBC_OPCODE_9E.serviceaction.READ_CAPACITY_16
    assert cdb[2:10] == bytearray(8)
    assert scsi_ba_to_int(cdb[10:14]) == 37
    assert cdb[14:16] == bytearray(2)
    cdb = r.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.SBC_OPCODE_9E.value
    assert cdb['service_action'] == s.device.opcodes.SBC_OPCODE_9E.serviceaction.READ_CAPACITY_16
    assert cdb['alloc_len'] == 37

if __name__ == "__main__":
    main()

