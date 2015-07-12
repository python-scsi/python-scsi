#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.utils.converter import scsi_ba_to_int
from mock_device import MockDevice
from pyscsi.pyscsi.scsi_cdb_positiontoelement import PositionToElement


class MockPositionToElement(MockDevice):
    pass


def main():
    dev = MockPositionToElement()
    dev.opcodes = smc
    s = SCSI(dev)
    s.device.opcodes = smc
    m = s.positiontoelement(15, 32, invert=1)
    cdb = m.cdb
    assert cdb[0] == s.device.opcodes.POSITION_TO_ELEMENT.value
    assert cdb[1] == 0
    assert scsi_ba_to_int(cdb[2:4]) == 15
    assert scsi_ba_to_int(cdb[4:6]) == 32
    assert cdb[8] == 0x01
    cdb = m.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.POSITION_TO_ELEMENT.value
    assert cdb['medium_transport_address'] == 15
    assert cdb['destination_address'] == 32
    assert cdb['invert'] == 1

    d = PositionToElement.unmarshall_cdb(PositionToElement.marshall_cdb(cdb))
    assert d == cdb

if __name__ == "__main__":
    main()


