#!/usr/bin/env python
# coding: utf-8

from pyscsi.pyscsi.scsi import SCSI
from mock_device import MockDevice
from pyscsi.utils.converter import scsi_int_to_ba
from pyscsi.pyscsi.scsi_enum_command import spc
from pyscsi.pyscsi import scsi_enum_modesense6 as MODESENSE6
from pyscsi.pyscsi.scsi_cdb_modesense6 import ModeSense6


class MockModeSenseEAA(MockDevice):
    def execute(self, cdb, dataout, datain, sense):
        datain[0] = 21  # mode data length
        datain[1] = 97  # medium type
        datain[2] = 98  # device specific parameter
        datain[3] = 0  # block descriptor length

        datain[4] = 0x9d  # PS=1 SPF=0 PAGECODE=0x1d
        datain[5] = 16    # Parameter List Length

        datain[6:8] = bytearray([1, 1])  # First Medium Transfer Element
        datain[8:10] = bytearray([1, 2])  # Num Medium Transfer Elements
        datain[10:12] = bytearray([1, 3])  # First Storage Element
        datain[12:14] = bytearray([1, 4])  # Num Storage Elements
        datain[14:16] = bytearray([1, 5])  # First Import Element
        datain[16:18] = bytearray([1, 6])  # Num Import Elements
        datain[18:20] = bytearray([1, 7])  # First Data Transport Element
        datain[20:22] = bytearray([1, 8])  # Num Data Transport Elements

class MockModeSenseControl(MockDevice):
    def execute(self, cdb, dataout, datain, sense):
        datain[0] = 15   # mode data length
        datain[1] = 0    # medium type: BLOCK_DEVICE
        datain[2] = 0x90 # device specific parameter
        datain[3] = 0    # block descriptor length

        datain[4] = 0x8a  # PS=1 SPF=0 PAGECODE=0x0a
        datain[5] = 10    # Parameter List Length

        datain[6] = 0x9f  # tst:4 tmdf_only:1 dpicz:1 d_Sense:1 gltsd:1 rlec:1
        datain[7] = 0x9e  # qam:9 nuar:1 qerr:3
        datain[8] = 0xf8  # vs:1 rac:1 uaic:3 swp:1
        datain[9] = 0xf7  # ato:1 tas:1 atmpe:1 rwwp:1 am:7
        datain[12:14] = scsi_int_to_ba(500, 2)  # busy timeout:500
        datain[14:16] = scsi_int_to_ba(700, 2)  # ext:700

def main():
    # SMC ElementAddressAssignment
    dev = MockModeSenseEAA()
    dev.opcodes = spc
    s = SCSI(dev)
    i = s.modesense6(page_code=MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT).result
    assert i['medium_type'] == 97
    assert i['device_specific_parameter'] == 98

    assert len(i['mode_pages']) == 1

    assert i['mode_pages'][0]['ps'] == 1
    assert i['mode_pages'][0]['spf'] == 0
    assert i['mode_pages'][0]['page_code'] == MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT
    assert i['mode_pages'][0]['first_medium_transport_element_address'] == 257
    assert i['mode_pages'][0]['num_medium_transport_elements'] == 258
    assert i['mode_pages'][0]['first_storage_element_address'] == 259
    assert i['mode_pages'][0]['num_storage_elements'] == 260
    assert i['mode_pages'][0]['first_import_element_address'] == 261
    assert i['mode_pages'][0]['num_import_elements'] == 262
    assert i['mode_pages'][0]['first_data_transfer_element_address'] == 263
    assert i['mode_pages'][0]['num_data_transfer_elements'] == 264

    d = ModeSense6.unmarshall_datain(ModeSense6.marshall_datain(i))
    assert d == i

    # SPC Control
    dev = MockModeSenseControl()
    dev.opcodes = spc
    s = SCSI(dev)
    i = s.modesense6(page_code=MODESENSE6.PAGE_CODE.CONTROL).result
    assert i['medium_type'] == 0
    assert i['device_specific_parameter'] == 0x90

    assert len(i['mode_pages']) == 1

    assert i['mode_pages'][0]['ps'] == 1
    assert i['mode_pages'][0]['spf'] == 0
    assert i['mode_pages'][0]['page_code'] == MODESENSE6.PAGE_CODE.CONTROL
    assert i['mode_pages'][0]['tst'] == 4
    assert i['mode_pages'][0]['tmf_only'] == 1
    assert i['mode_pages'][0]['dpicz'] == 1
    assert i['mode_pages'][0]['d_sense'] == 1
    assert i['mode_pages'][0]['gltsd'] == 1
    assert i['mode_pages'][0]['rlec'] == 1
    assert i['mode_pages'][0]['queue_algorithm_modifier'] == 9
    assert i['mode_pages'][0]['nuar'] == 1
    assert i['mode_pages'][0]['qerr'] == 3
    assert i['mode_pages'][0]['vs'] == 1
    assert i['mode_pages'][0]['rac'] == 1
    assert i['mode_pages'][0]['ua_intlck_ctrl'] == 3
    assert i['mode_pages'][0]['swp'] == 1
    assert i['mode_pages'][0]['ato'] == 1
    assert i['mode_pages'][0]['tas'] == 1
    assert i['mode_pages'][0]['atmpe'] == 1
    assert i['mode_pages'][0]['rwwp'] == 1
    assert i['mode_pages'][0]['autoload_mode'] == 7
    assert i['mode_pages'][0]['busy_timeout_period'] == 500
    assert i['mode_pages'][0]['extended_self_test_completion_time'] == 700

    d = ModeSense6.unmarshall_datain(ModeSense6.marshall_datain(i))
    assert d == i

if __name__ == "__main__":
    main()

