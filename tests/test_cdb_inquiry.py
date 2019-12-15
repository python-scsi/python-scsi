#!/usr/bin/env python
# coding: utf-8
from pyscsi.utils.converter import scsi_ba_to_int
from pyscsi.pyscsi.scsi_enum_command import spc
from pyscsi.pyscsi.scsi_cdb_inquiry import Inquiry
from mock_device import MockDevice, MockSCSI


def main():
    with MockSCSI(MockDevice(spc)) as s:
        # cdb for standard page request
        i = s.inquiry(alloclen=128)
        cdb = i.cdb
        assert cdb[0] == s.device.opcodes.INQUIRY.value
        assert cdb[1:3] == bytearray(2)
        assert scsi_ba_to_int(cdb[3:5]) == 128
        assert cdb[5] == 0
        cdb = i.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.INQUIRY.value
        assert cdb['evpd'] == 0
        assert cdb['page_code'] == 0
        assert cdb['alloc_len'] == 128

        d = Inquiry.unmarshall_cdb(Inquiry.marshall_cdb(cdb))
        assert d == cdb

        # supported vpd pages
        i = s.inquiry(evpd=1, page_code=0x88, alloclen=300)
        cdb = i.cdb
        assert cdb[0] == s.device.opcodes.INQUIRY.value
        assert cdb[1] == 0x01
        assert cdb[2] == 0x88
        assert scsi_ba_to_int(cdb[3:5]) == 300
        assert cdb[5] == 0
        cdb = i.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.INQUIRY.value
        assert cdb['evpd'] == 1
        assert cdb['page_code'] == 0x88
        assert cdb['alloc_len'] == 300

        d = Inquiry.unmarshall_cdb(Inquiry.marshall_cdb(cdb))
        assert d == cdb


if __name__ == "__main__":
    main()

