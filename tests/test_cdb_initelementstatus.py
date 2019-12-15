#!/usr/bin/env python
# coding: utf-8
from pyscsi.pyscsi.scsi_enum_command import smc
from mock_device import MockDevice, MockSCSI
from pyscsi.pyscsi.scsi_cdb_initelementstatus import InitializeElementStatus


def main():
    with MockSCSI(MockDevice(smc)) as s:
        r = s.initializeelementstatus()
        cdb = r.cdb
        assert cdb[0] == s.device.opcodes.INITIALIZE_ELEMENT_STATUS.value
        cdb = r.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.INITIALIZE_ELEMENT_STATUS.value

        d = InitializeElementStatus.unmarshall_cdb(InitializeElementStatus.marshall_cdb(cdb))
        assert d == cdb


if __name__ == "__main__":
    main()



