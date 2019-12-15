#!/usr/bin/env python
# coding: utf-8
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_cdb_write16 import Write16
from mock_device import MockDevice, MockSCSI


def main():

    with MockSCSI(MockDevice(sbc)) as s:
        s.blocksize = 512

        data = bytearray(27 * 512)

        w = s.write16(1024, 27, data)
        cdb = w.cdb
        assert cdb[0] == s.device.opcodes.WRITE_16.value
        assert cdb[1] == 0
        assert scsi_ba_to_int(cdb[2:10]) == 1024
        assert scsi_ba_to_int(cdb[10:14]) == 27
        assert cdb[14] == 0
        assert cdb[15] == 0
        cdb = w.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.WRITE_16.value
        assert cdb['wrprotect'] == 0
        assert cdb['dpo'] == 0
        assert cdb['fua'] == 0
        assert cdb['lba'] == 1024
        assert cdb['group'] == 0
        assert cdb['tl'] == 27

        d = Write16.unmarshall_cdb(Write16.marshall_cdb(cdb))
        assert d == cdb

        w = s.write16(65536, 27, data, wrprotect=2, dpo=1, fua=1, group=19)
        cdb = w.cdb
        assert cdb[0] == s.device.opcodes.WRITE_16.value
        assert cdb[1] == 0x58
        assert scsi_ba_to_int(cdb[2:10]) == 65536
        assert scsi_ba_to_int(cdb[10:14]) == 27
        assert cdb[14] == 0x13
        assert cdb[15] == 0
        cdb = w.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.WRITE_16.value
        assert cdb['wrprotect'] == 2
        assert cdb['dpo'] == 1
        assert cdb['fua'] == 1
        assert cdb['lba'] == 65536
        assert cdb['group'] == 19
        assert cdb['tl'] == 27

        d = Write16.unmarshall_cdb(Write16.marshall_cdb(cdb))
        assert d == cdb


if __name__ == "__main__":
    main()

