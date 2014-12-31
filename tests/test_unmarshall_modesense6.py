#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from pyscsi.pyscsi import scsi_enum_modesense6 as MODESENSE6


class MockModeSenseEAA(object):
    def execute(self, cdb, dataout, datain, sense):
        datain[0] = 96  # mode data length
        datain[1] = 97  # medium type
        datain[2] = 98  # device specific parameter
        datain[3] = 0  # block descriptor length

        datain[4] = 0xdd  # PS=1 SPF=1 PAGECODE=0x1d
        datain[5] = 16    # Parameter List Length
        datain[6:8] = bytearray([1, 1])  # First Medium Transfer Element
        datain[8:10] = bytearray([1, 2])  # Num Medium Transfer Elements
        datain[10:12] = bytearray([1, 3])  # First Storage Element
        datain[12:14] = bytearray([1, 4])  # Num Storage Elements
        datain[14:16] = bytearray([1, 5])  # First Import Element
        datain[16:18] = bytearray([1, 6])  # Num Import Elements
        datain[18:20] = bytearray([1, 7])  # First Data Transport Element
        datain[20:22] = bytearray([1, 8])  # Num Data Transport Elements


def main():
    s = SCSI(MockModeSenseEAA())

    # SMC ElementAddressAssignment
    i = s.modesense6(page_code=MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT).result
    assert i['mode_data_length'] == 96
    assert i['medium_type'] == 97
    assert i['device_specific_parameter'] == 98
    assert i['block_descriptor_length'] == 0

    assert i['ps'] == 1
    assert i['spf'] == 1
    assert i['page_code'] == MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT
    assert i['parameter_list_length'] == 16
    assert i['first_medium_transport_element_address'] == 257
    assert i['num_medium_transport_elements'] == 258
    assert i['first_storage_element_address'] == 259
    assert i['num_storage_elements'] == 260
    assert i['first_import_element_address'] == 261
    assert i['num_import_elements'] == 262
    assert i['first_data_transfer_element_address'] == 263
    assert i['num_data_transfer_elements'] == 264

if __name__ == "__main__":
    main()

