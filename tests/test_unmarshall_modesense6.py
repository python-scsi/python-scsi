# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi import scsi_enum_modesense as MODESENSE6
from pyscsi.pyscsi.scsi_cdb_modesense6 import ModeSense6
from pyscsi.pyscsi.scsi_enum_command import spc
from pyscsi.utils.converter import scsi_int_to_ba

from .mock_device import MockDevice, MockSCSI


class MockModeSenseEAA(MockDevice):

    def execute(self, cmd):
        cmd.datain[0] = 21  # mode data length
        cmd.datain[1] = 97  # medium type
        cmd.datain[2] = 98  # device specific parameter
        cmd.datain[3] = 0  # block descriptor length

        cmd.datain[4] = 0x9d  # PS=1 SPF=0 PAGECODE=0x1d
        cmd.datain[5] = 16    # Parameter List Length

        cmd.datain[6:8] = bytearray([1, 1])  # First Medium Transfer Element
        cmd.datain[8:10] = bytearray([1, 2])  # Num Medium Transfer Elements
        cmd.datain[10:12] = bytearray([1, 3])  # First Storage Element
        cmd.datain[12:14] = bytearray([1, 4])  # Num Storage Elements
        cmd.datain[14:16] = bytearray([1, 5])  # First Import Element
        cmd.datain[16:18] = bytearray([1, 6])  # Num Import Elements
        cmd.datain[18:20] = bytearray([1, 7])  # First Data Transport Element
        cmd.datain[20:22] = bytearray([1, 8])  # Num Data Transport Elements


class MockModeSenseControl(MockDevice):

    def execute(self, cmd):
        cmd.datain[0] = 15    # mode data length
        cmd.datain[1] = 0     # medium type: BLOCK_DEVICE
        cmd.datain[2] = 0x90  # device specific parameter
        cmd.datain[3] = 0     # block descriptor length

        cmd.datain[4] = 0x8a  # PS=1 SPF=0 PAGECODE=0x0a
        cmd.datain[5] = 10    # Parameter List Length

        cmd.datain[6] = 0x9f  # tst:4 tmdf_only:1 dpicz:1 d_Sense:1 gltsd:1 rlec:1
        cmd.datain[7] = 0x9e  # qam:9 nuar:1 qerr:3
        cmd.datain[8] = 0xf8  # vs:1 rac:1 uaic:3 swp:1
        cmd.datain[9] = 0xf7  # ato:1 tas:1 atmpe:1 rwwp:1 am:7
        cmd.datain[12:14] = scsi_int_to_ba(500, 2)  # busy timeout:500
        cmd.datain[14:16] = scsi_int_to_ba(700, 2)  # ext:700


class MockModeSenseControlExt1(MockDevice):

    def execute(self, cmd):
        cmd.datain[0] = 15    # mode data length
        cmd.datain[1] = 0     # medium type: BLOCK_DEVICE
        cmd.datain[2] = 0x90  # device specific parameter
        cmd.datain[3] = 0     # block descriptor length

        cmd.datain[4] = 0xca                       # PS=1 SPF=1 PAGECODE=0x0a
        cmd.datain[5] = 1                          # subpage:1
        cmd.datain[6:8] = scsi_int_to_ba(0x1c, 2)  # page length

        cmd.datain[8] = 0x07  # tcmod:1 scsip:1 ialuae:1
        cmd.datain[9] = 0x0f  # icp:15
        cmd.datain[10] = 29   # msdl:29


class MockModeSenseDisconnect(MockDevice):

    def execute(self, cmd):
        cmd.datain[0] = 15    # mode data length
        cmd.datain[1] = 0     # medium type: BLOCK_DEVICE
        cmd.datain[2] = 0x90  # device specific parameter
        cmd.datain[3] = 0     # block descriptor length

        cmd.datain[4] = 0x82  # PS=1 SPF=0 PAGECODE=0x02
        cmd.datain[5] = 0x0e

        cmd.datain[6] = 122                          # bfr:122
        cmd.datain[7] = 123                          # ber:123
        cmd.datain[8:10] = scsi_int_to_ba(2371, 2)   # bil
        cmd.datain[10:12] = scsi_int_to_ba(2372, 2)  # dtl
        cmd.datain[12:14] = scsi_int_to_ba(2373, 2)  # ctl
        cmd.datain[14:16] = scsi_int_to_ba(2374, 2)  # mbs
        cmd.datain[16] = 0xff                        # emdp:1 fa:7 dimm:1 dtdc:7
        cmd.datain[18:20] = scsi_int_to_ba(2375, 2)  # fbs

class unmarshallModesense6Test(unittest.TestCase):
    def test_main(self):
        # SMC ElementAddressAssignment
        with MockSCSI(MockModeSenseEAA(spc)) as s:
            i = s.modesense6(page_code=MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT).result
            self.assertEqual(i['medium_type'], 97)
            self.assertEqual(i['device_specific_parameter'], 98)

            self.assertEqual(len(i['mode_pages']), 1)

            self.assertEqual(i['mode_pages'][0]['ps'], 1)
            self.assertEqual(i['mode_pages'][0]['spf'], 0)
            self.assertEqual(i['mode_pages'][0]['page_code'], MODESENSE6.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT)
            self.assertEqual(i['mode_pages'][0]['first_medium_transport_element_address'], 257)
            self.assertEqual(i['mode_pages'][0]['num_medium_transport_elements'], 258)
            self.assertEqual(i['mode_pages'][0]['first_storage_element_address'], 259)
            self.assertEqual(i['mode_pages'][0]['num_storage_elements'], 260)
            self.assertEqual(i['mode_pages'][0]['first_import_element_address'], 261)
            self.assertEqual(i['mode_pages'][0]['num_import_elements'], 262)
            self.assertEqual(i['mode_pages'][0]['first_data_transfer_element_address'], 263)
            self.assertEqual(i['mode_pages'][0]['num_data_transfer_elements'], 264)

            d = ModeSense6.unmarshall_datain(ModeSense6.marshall_datain(i))
            self.assertEqual(d, i)

            # SPC Control
            s.device = MockModeSenseControl(spc)
            i = s.modesense6(page_code=MODESENSE6.PAGE_CODE.CONTROL).result
            self.assertEqual(i['medium_type'], 0)
            self.assertEqual(i['device_specific_parameter'], 0x90)

            self.assertEqual(len(i['mode_pages']), 1)

            self.assertEqual(i['mode_pages'][0]['ps'], 1)
            self.assertEqual(i['mode_pages'][0]['spf'], 0)
            self.assertEqual(i['mode_pages'][0]['page_code'], MODESENSE6.PAGE_CODE.CONTROL)
            self.assertEqual(i['mode_pages'][0]['tst'], 4)
            self.assertEqual(i['mode_pages'][0]['tmf_only'], 1)
            self.assertEqual(i['mode_pages'][0]['dpicz'], 1)
            self.assertEqual(i['mode_pages'][0]['d_sense'], 1)
            self.assertEqual(i['mode_pages'][0]['gltsd'], 1)
            self.assertEqual(i['mode_pages'][0]['rlec'], 1)
            self.assertEqual(i['mode_pages'][0]['queue_algorithm_modifier'], 9)
            self.assertEqual(i['mode_pages'][0]['nuar'], 1)
            self.assertEqual(i['mode_pages'][0]['qerr'], 3)
            self.assertEqual(i['mode_pages'][0]['vs'], 1)
            self.assertEqual(i['mode_pages'][0]['rac'], 1)
            self.assertEqual(i['mode_pages'][0]['ua_intlck_ctrl'], 3)
            self.assertEqual(i['mode_pages'][0]['swp'], 1)
            self.assertEqual(i['mode_pages'][0]['ato'], 1)
            self.assertEqual(i['mode_pages'][0]['tas'], 1)
            self.assertEqual(i['mode_pages'][0]['atmpe'], 1)
            self.assertEqual(i['mode_pages'][0]['rwwp'], 1)
            self.assertEqual(i['mode_pages'][0]['autoload_mode'], 7)
            self.assertEqual(i['mode_pages'][0]['busy_timeout_period'], 500)
            self.assertEqual(i['mode_pages'][0]['extended_self_test_completion_time'], 700)

            d = ModeSense6.unmarshall_datain(ModeSense6.marshall_datain(i))
            self.assertEqual(d, i)

            # SPC Control Ext 1
            s.device = MockModeSenseControlExt1(spc)
            i = s.modesense6(page_code=MODESENSE6.PAGE_CODE.CONTROL, sub_page_code=1).result
            self.assertEqual(i['medium_type'], 0)
            self.assertEqual(i['device_specific_parameter'], 0x90)

            self.assertEqual(len(i['mode_pages']), 1)

            self.assertEqual(i['mode_pages'][0]['ps'], 1)
            self.assertEqual(i['mode_pages'][0]['spf'], 1)
            self.assertEqual(i['mode_pages'][0]['page_code'], MODESENSE6.PAGE_CODE.CONTROL)
            self.assertEqual(i['mode_pages'][0]['sub_page_code'], 1)
            self.assertEqual(i['mode_pages'][0]['tcmos'], 1)
            self.assertEqual(i['mode_pages'][0]['scsip'], 1)
            self.assertEqual(i['mode_pages'][0]['ialuae'], 1)
            self.assertEqual(i['mode_pages'][0]['initial_command_priority'], 15)
            self.assertEqual(i['mode_pages'][0]['maximum_sense_data_length'], 29)

            d = ModeSense6.unmarshall_datain(ModeSense6.marshall_datain(i))
            self.assertEqual(d, i)

            # SPC Disconnect
            s.device = MockModeSenseDisconnect(spc)
            i = s.modesense6(page_code=MODESENSE6.PAGE_CODE.DISCONNECT_RECONNECT).result
            self.assertEqual(i['medium_type'], 0)
            self.assertEqual(i['device_specific_parameter'], 0x90)

            self.assertEqual(len(i['mode_pages']), 1)

            self.assertEqual(i['mode_pages'][0]['ps'], 1)
            self.assertEqual(i['mode_pages'][0]['spf'], 0)
            self.assertEqual(i['mode_pages'][0]['page_code'], MODESENSE6.PAGE_CODE.DISCONNECT_RECONNECT)
            self.assertEqual(i['mode_pages'][0]['buffer_full_ratio'], 122)
            self.assertEqual(i['mode_pages'][0]['buffer_empty_ratio'], 123)
            self.assertEqual(i['mode_pages'][0]['bus_inactivity_limit'], 2371)
            self.assertEqual(i['mode_pages'][0]['disconnect_time_limit'], 2372)
            self.assertEqual(i['mode_pages'][0]['connect_time_limit'], 2373)
            self.assertEqual(i['mode_pages'][0]['maximum_burst_size'], 2374)
            self.assertEqual(i['mode_pages'][0]['emdp'], 1)
            self.assertEqual(i['mode_pages'][0]['fair_arbitration'], 7)
            self.assertEqual(i['mode_pages'][0]['dimm'], 1)
            self.assertEqual(i['mode_pages'][0]['dtdc'], 7)
            self.assertEqual(i['mode_pages'][0]['first_burst_size'], 2375)

            d = ModeSense6.unmarshall_datain(ModeSense6.marshall_datain(i))
            self.assertEqual(d, i)
