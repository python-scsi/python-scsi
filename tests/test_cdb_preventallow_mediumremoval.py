#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import smc
from mock_device import MockDevice
from pyscsi.pyscsi.scsi_cdb_preventallow_mediumremoval import PreventAllowMediumRemoval


class MockPreventAllowMediumRemoval(MockDevice):
    pass


def main():
    dev = MockPreventAllowMediumRemoval()
    dev.opcodes = smc
    s = SCSI(dev)
    s.device.opcodes = smc
    m = s.preventallowmediumremoval(prevent=3)
    cdb = m.cdb
    assert cdb[0] == s.device.opcodes.PREVENT_ALLOW_MEDIUM_REMOVAL.value
    assert cdb[8] == 0x03
    cdb = m.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.PREVENT_ALLOW_MEDIUM_REMOVAL.value
    assert cdb['prevent'] == 3

    d = PreventAllowMediumRemoval.unmarshall_cdb(PreventAllowMediumRemoval.marshall_cdb(cdb))
    assert d == cdb

if __name__ == "__main__":
    main()
