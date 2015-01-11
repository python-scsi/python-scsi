#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi_enum_command import spc, sbc, ssc, smc


def main():
    _spc = spc
    _sbc = sbc
    _ssc = ssc
    _smc = smc

    assert _spc.opcode.SET_DEVICE_IDENTIFIER.value == 0xa4
    assert _sbc.opcode.READ_CAPACITY_16.value == 0x9e
    assert _ssc.opcode.READ_ELEMENT_STATUS_ATTACHED == 0xb4

if __name__ == "__main__":
    main()
