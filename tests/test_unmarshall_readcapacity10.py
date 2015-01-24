#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import sbc
from mock_device import MockDevice


class MockReadCapacity10(MockDevice):
    def execute(self, cdb, dataout, datain, sense):
        # lba
        datain[0:4] = [0x00, 0x01, 0x00, 0x00]
        # block size
        datain[4:8] = [0x00, 0x00, 0x10, 0x00]


def main():
    dev = MockReadCapacity10()
    dev.opcodes = sbc
    s = SCSI(dev)

    i = s.readcapacity10().result
    assert i['returned_lba'] == 65536
    assert i['block_length'] == 4096

if __name__ == "__main__":
    main()

