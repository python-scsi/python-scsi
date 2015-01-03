#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi_enum_command import SPC, SBC, SSC


def main():
    spc = SPC()
    sbc = SBC()
    ssc = SSC()

    assert spc.opcode.SET_DEVICE_IDENTIFIER == 0xa4
    assert spc.serviceaction.REPORT_SUPPORTED_OPERATION_CODES == 0x0c

    assert sbc.opcode.READ_CAPACITY_16 == 0x9e
    assert sbc.serviceaction.SET_IDENTIFYING_INFORMATION == 0x06

    assert ssc.opcode.READ_ELEMENT_STATUS_ATTACHED == 0xb4
    assert ssc.serviceaction.REPORT_SUPPORTED_OPERATION_CODES == 0x0c


if __name__ == "__main__":
    main()
