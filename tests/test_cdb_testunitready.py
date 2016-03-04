#!/usr/bin/env python
# coding: utf-8
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.pyscsi.scsi_cdb_testunitready import TestUnitReady
from mock_device import MockDevice, MockSCSI


def main():

    with MockSCSI(MockDevice(sbc)) as s:
        w = s.testunitready()
        cdb = w.cdb
        assert cdb[0] == s.device.opcodes.TEST_UNIT_READY.value
        assert cdb[1] == 0
        assert cdb[2] == 0
        assert cdb[3] == 0
        assert cdb[4] == 0
        assert cdb[5] == 0
        cdb = w.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.TEST_UNIT_READY.value

        d = TestUnitReady.unmarshall_cdb(TestUnitReady.marshall_cdb(cdb))
        assert d == cdb

if __name__ == "__main__":
    main()

