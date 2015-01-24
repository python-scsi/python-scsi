#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_enum_command import sbc
from mock_device import MockDevice


class MockGetLBAStatus(MockDevice):
    pass


def main():
    dev = MockGetLBAStatus()
    dev.opcodes = sbc
    s = SCSI(dev)

    r = s.getlbastatus(19938722, alloclen=1112527)
    cdb = r.cdb
    assert cdb[0] == s.device.opcodes.SBC_OPCODE_9E.value
    assert cdb[1] == s.device.opcodes.SBC_OPCODE_9E.serviceaction.GET_LBA_STATUS
    assert scsi_ba_to_int(cdb[2:10]) == 19938722
    assert scsi_ba_to_int(cdb[10:14]) == 1112527
    assert cdb[14:16] == bytearray(2)
    cdb = r.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.SBC_OPCODE_9E.value
    assert cdb['service_action'] == s.device.opcodes.SBC_OPCODE_9E.serviceaction.GET_LBA_STATUS
    assert cdb['lba'] == 19938722
    assert cdb['alloc_len'] == 1112527

if __name__ == "__main__":
    main()


