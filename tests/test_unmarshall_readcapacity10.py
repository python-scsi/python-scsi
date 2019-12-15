#!/usr/bin/env python
# coding: utf-8
from mock_device import MockDevice, MockSCSI
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.pyscsi.scsi_cdb_readcapacity10 import ReadCapacity10


class MockReadCapacity10(MockDevice):

    def execute(self, cmd):
        # lba
        cmd.datain[0:4] = [0x00, 0x01, 0x00, 0x00]
        # block size
        cmd.datain[4:8] = [0x00, 0x00, 0x10, 0x00]


def main():
    with MockSCSI(MockReadCapacity10(sbc)) as s:
        i = s.readcapacity10().result
        assert i['returned_lba'] == 65536
        assert i['block_length'] == 4096

        d = ReadCapacity10.unmarshall_datain(ReadCapacity10.marshall_datain(i))
        assert d == i


if __name__ == "__main__":
    main()

