#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi.scsi_enum_command import smc
from mock_device import MockDevice
from pyscsi.pyscsi.scsi_cdb_initelementstatus import InitializeElementStatus


class MockInitializeElementStatus(MockDevice):
    pass


def main():
    dev = MockInitializeElementStatus()
    dev.opcodes = smc
    s = SCSI(dev)
    # we need to reassign the right enum again because the MockDevice will return the wrong
    # peripheral_device_type and therefor assign the spc enum instead of smc.
    s.device.opcodes = smc

    r = s.initializeelementstatus()
    cdb = r.cdb
    assert cdb[0] == s.device.opcodes.INITIALIZE_ELEMENT_STATUS.value
    cdb = r.unmarshall_cdb(cdb)
    assert cdb['opcode'] == s.device.opcodes.INITIALIZE_ELEMENT_STATUS.value

    d = InitializeElementStatus.unmarshall_cdb(InitializeElementStatus.marshall_cdb(cdb))
    assert d == cdb

if __name__ == "__main__":
    main()



