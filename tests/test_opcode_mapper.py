#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi_enum_command import spc, sbc, ssc, smc


def main():
    _spc = spc
    _sbc = sbc
    _ssc = ssc
    _smc = smc

    assert _spc.SET_DEVICE_IDENTIFIER.value == 0xa4
    assert _sbc.READ_CAPACITY_16.value == 0x9e
    assert _ssc.READ_ELEMENT_STATUS_ATTACHED.value == 0xb4
    assert _smc.MAINTENANCE_IN.value == 0xa3
    assert _smc.MAINTENANCE_IN.serviceaction.REPORT_DEVICE_IDENTIFICATION == 0x07
    
if __name__ == "__main__":
    main()