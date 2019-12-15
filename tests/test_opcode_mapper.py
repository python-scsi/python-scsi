#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi_enum_command import spc, sbc, ssc, smc


def main():
    assert spc.SPC_OPCODE_A4.value == 0xa4
    assert sbc.SBC_OPCODE_9E.value == 0x9e
    assert ssc.READ_ELEMENT_STATUS_ATTACHED.value == 0xb4
    assert smc.MAINTENANCE_IN.value == 0xa3
    assert smc.MAINTENANCE_IN.serviceaction.REPORT_DEVICE_IDENTIFICATION == 0x07


if __name__ == "__main__":
    main()
