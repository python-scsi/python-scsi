#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.pyscsi.scsi_cdb_testunitready import TestUnitReady


class MockTestUnitReady(object):
    def execute(self, cdb, dataout, datain, sense):
        pass


def main():
    dev = MockTestUnitReady()
    dev.opcodes = sbc
    s = SCSI(dev)

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

