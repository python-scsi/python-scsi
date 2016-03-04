#!/usr/bin/env python
# coding: utf-8
from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.utils.converter import scsi_ba_to_int
from mock_device import MockDevice, MockSCSI
from pyscsi.pyscsi.scsi_cdb_exchangemedium import ExchangeMedium


def main():
    with MockSCSI(MockDevice(smc)) as s:
        m = s.exchangemedium(15, 32, 64, 32, inv1=1)
        cdb = m.cdb
        assert cdb[0] == s.device.opcodes.EXCHANGE_MEDIUM.value
        assert cdb[1] == 0
        assert scsi_ba_to_int(cdb[2:4]) == 15
        assert scsi_ba_to_int(cdb[4:6]) == 32
        assert scsi_ba_to_int(cdb[6:8]) == 64
        assert scsi_ba_to_int(cdb[8:10]) == 32
        assert cdb[10] == 0x02
        cdb = m.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.EXCHANGE_MEDIUM.value
        assert cdb['medium_transport_address'] == 15
        assert cdb['source_address'] == 32
        assert cdb['first_destination_address'] == 64
        assert cdb['second_destination_address'] == 32
        assert cdb['inv1'] == 1
        assert cdb['inv2'] == 0

        d = ExchangeMedium.unmarshall_cdb(ExchangeMedium.marshall_cdb(cdb))
        assert d == cdb

if __name__ == "__main__":
    main()

