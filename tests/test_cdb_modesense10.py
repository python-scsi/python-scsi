#!/usr/bin/env python
# coding: utf-8
from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.pyscsi import scsi_enum_modesense as MODESENSE10
from pyscsi.pyscsi.scsi_cdb_modesense10 import ModeSense10
from pyscsi.utils.converter import scsi_ba_to_int
from mock_device import MockDevice, MockSCSI


def main():
    with MockSCSI(MockDevice(smc)) as s:
        # cdb for SMC: ElementAddressAssignment
        m = s.modesense10(page_code=MODESENSE10.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT)
        cdb = m.cdb
        assert cdb[0] == s.device.opcodes.MODE_SENSE_10.value
        assert cdb[1] == 0
        assert cdb[2] == MODESENSE10.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT
        assert cdb[3] == 0
        assert cdb[4:6] == bytearray(2)
        assert scsi_ba_to_int(cdb[7:9]) == 96
        assert cdb[9] == 0
        cdb = m.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.MODE_SENSE_10.value
        assert cdb['dbd'] == 0
        assert cdb['llbaa'] == 0
        assert cdb['page_code'] == MODESENSE10.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT
        assert cdb['pc'] == 0
        assert cdb['sub_page_code'] == 0
        assert cdb['alloc_len'] == 96

        d = ModeSense10.unmarshall_cdb(ModeSense10.marshall_cdb(cdb))
        assert d == cdb

        m = s.modesense10(page_code=0, sub_page_code=3, llbaa=1, dbd=1, pc=MODESENSE10.PC.DEFAULT, alloclen=90)
        cdb = m.cdb
        assert cdb[0] == s.device.opcodes.MODE_SENSE_10.value
        assert cdb[1] == 0x18
        assert cdb[2] == MODESENSE10.PC.DEFAULT << 6
        assert cdb[3] == 3
        assert scsi_ba_to_int(cdb[7:9]) == 90
        cdb = m.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.MODE_SENSE_10.value
        assert cdb['dbd'] == 1
        assert cdb['pc'] == MODESENSE10.PC.DEFAULT
        assert cdb['page_code'] == 0
        assert cdb['sub_page_code'] == 3
        assert cdb['alloc_len'] == 90
        assert cdb['llbaa'] == 1

        d = ModeSense10.unmarshall_cdb(ModeSense10.marshall_cdb(cdb))
        assert d == cdb


if __name__ == "__main__":
    main()