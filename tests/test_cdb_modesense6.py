#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import spc
from pyscsi.pyscsi import scsi_enum_modesense6 as MODESENSE6
from pyscsi.pyscsi.scsi_cdb_modesense6 import ModeSense6


class MockModeSense6(object):
    def execute(self, cdb, dataout, datain, sense):
        pass


def main():
    dev = MockModeSense6()
    dev.opcodes = spc
    s = SCSI(dev)

    # cdb for SMC: ElementAddressAssignment
    m = s.modesense6(page_code=MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT)
    cdb = m.cdb
    assert cdb[0] == s.device.opcodes.MODE_SENSE_6.value
    assert cdb[1] == 0
    assert cdb[2] == MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT
    assert cdb[3] == 0
    assert cdb[4] == 96
    assert cdb[5] == 0
    cdb = m.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.MODE_SENSE_6.value
    assert cdb['dbd'] == 0
    assert cdb['pc'] == 0
    assert cdb['page_code'] == MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT
    assert cdb['sub_page_code'] == 0
    assert cdb['alloc_len'] == 96

    d = ModeSense6.unmarshall_cdb(ModeSense6.marshall_cdb(cdb))
    assert d == cdb

    m = s.modesense6(page_code=0, sub_page_code=3, dbd=1, pc=MODESENSE6.PC.DEFAULT, alloclen=90)
    cdb = m.cdb
    assert cdb[0] == s.device.opcodes.MODE_SENSE_6.value
    assert cdb[1] == 0x08
    assert cdb[2] == MODESENSE6.PC.DEFAULT << 6
    assert cdb[3] == 3
    assert cdb[4] == 90
    assert cdb[5] == 0
    cdb = m.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.MODE_SENSE_6.value
    assert cdb['dbd'] == 1
    assert cdb['pc'] == MODESENSE6.PC.DEFAULT
    assert cdb['page_code'] == 0
    assert cdb['sub_page_code'] == 3
    assert cdb['alloc_len'] == 90

    d = ModeSense6.unmarshall_cdb(ModeSense6.marshall_cdb(cdb))
    assert d == cdb

if __name__ == "__main__":
    main()

