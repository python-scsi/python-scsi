#!/usr/bin/env python
# coding: utf-8

from sgio.pyscsi.scsi import SCSI


class MockReadCapacity16(object):
    def execute(self, cdb, dataout, datain, sense):
        # lba
        datain[0:8] = [0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        # block size
        datain[8:12] = [0x00, 0x00, 0x10, 0x00]
        datain[12] = 0x09  # P_TYPE:4 PROT_EN:1
        datain[13] = 0x88  # P_I_EXPONENT:8 LBPPBE:8
        datain[14] = 0xe0  # LBPME:1 LBPRZ:1 LOWEST_ALIGNED_LBA:top-bit-set
        datain[15] = 0x01  # LOWEST_ALIGNED_LBA:bottom-bit-set


def main():
    s = SCSI(MockReadCapacity16())

    i = s.readcapacity16().result
    assert i['returned_lba'] == 281474976710656
    assert i['block_length'] == 4096
    assert i['p_type'] == 4
    assert i['prot_en'] == 1
    assert i['p_i_exponent'] == 8
    assert i['lbppbe'] == 8
    assert i['lbpme'] == 1
    assert i['lbprz'] == 1
    assert i['lowest_aligned_lba'] == 8193

if __name__ == "__main__":
    main()

