#!/usr/bin/env python
# coding: utf-8
from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.utils.converter import scsi_ba_to_int
from mock_device import MockDevice, MockSCSI
from pyscsi.pyscsi.scsi_cdb_initelementstatuswithrange import InitializeElementStatusWithRange


class MockInitializeElementStatusWithRange(MockDevice):
    pass


def main():
    with MockSCSI(MockDevice(smc)) as s:
        r = s.initializeelementstatuswithrange(15, 3, rng=1, fast=1)
        cdb = r.cdb
        assert cdb[0] == s.device.opcodes.INITIALIZE_ELEMENT_STATUS_WITH_RANGE.value
        assert cdb[1] == 0x03
        assert scsi_ba_to_int(cdb[2:4]) == 15
        assert scsi_ba_to_int(cdb[6:8]) == 3

        cdb = r.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.INITIALIZE_ELEMENT_STATUS_WITH_RANGE.value
        assert cdb['starting_element_address'] == 15
        assert cdb['number_of_elements'] == 3
        assert cdb['fast'] == 1
        assert cdb['range'] == 1

        d = InitializeElementStatusWithRange.unmarshall_cdb(InitializeElementStatusWithRange.marshall_cdb(cdb))
        assert d == cdb

if __name__ == "__main__":
    main()
