# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi import scsi_enum_inquiry as INQUIRY
from pyscsi.pyscsi.scsi_cdb_inquiry import Inquiry
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.utils.converter import scsi_int_to_ba

from .mock_device import MockDevice, MockSCSI


class MockInquiryStandard(MockDevice):

    def execute(self, cmd):
        cmd.datain[0] = 0x25  # QUAL:1 TYPE:5
        cmd.datain[1] = 0x80  # RMB:1
        cmd.datain[2] = 0x07  # VERSION:7
        cmd.datain[3] = 0x23  # NORMACA:1 HISUP:0 RDF:3
        cmd.datain[4] = 0x40  # ADDITIONAL LENGTH:64
        cmd.datain[5] = 0xb9  # SCCS:1 ACC:0 TGPS:3 3PC:1 PROTECT:1
        cmd.datain[6] = 0x71  # ENCSERV:1 VS:1 MULTIP:1 ADDR16:1
        cmd.datain[7] = 0x33  # WBUS16:1 SYNC:1 CMDQUE:1 VS2:1
        # t10 vendor id
        cmd.datain[8:16] = bytearray(ord(c) for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        # product id
        cmd.datain[16:32] = bytearray(ord(c) for c in ['i', 'i', 'i', 'i', 'i', 'i', 'i', 'i',
                         'j', 'j', 'j', 'j', 'j', 'j', 'j', 'j'])
        # product revision level
        cmd.datain[32:36] = bytearray(ord(c) for c in ['r', 'e', 'v', 'n'])
        cmd.datain[56] = 0x09  # CLOCKING:2 QAS:0 IUS:1


class MockLBP(MockDevice):

    def execute(self, cmd):
        cmd.datain[0] = 0x00  # QUAL:0 TYPE:0
        cmd.datain[1] = 0xb2  # logical block provisioning
        cmd.datain[2] = 0x00  #
        cmd.datain[3] = 0x04  # page length == 4
        cmd.datain[4] = 0x12  # threshold exponent
        cmd.datain[5] = 0xe7  # LBPU:1 LBPWS:1 LBPWS10:1 LBPRZ:1 ANC_SUP:1 DP:1
        cmd.datain[6] = 0x02  # Provisioning Type:2
        cmd.datain[7] = 0x00  #


class MockUSN(MockDevice):

    def execute(self, cmd):
        cmd.datain[0] = 0x00  # QUAL:0 TYPE:0
        cmd.datain[1] = 0x80  # unit serial number
        cmd.datain[2] = 0x00  #
        cmd.datain[3] = 0x04  # page length == 4
        cmd.datain[4:8] = "ABCD".encode()


class MockDevId(MockDevice):

    def execute(self, cmd):
        cmd.datain[0] = 0x00  # QUAL:0 TYPE:0
        cmd.datain[1] = 0x83  # device identifier
        cmd.datain[2] = 0x00
        cmd.datain[3] = 0x00
        pos = 4

        # Designation Descriptor: T10_VENDOR_ID
        t10 = bytearray(8)
        t10[0] = ord('T')
        t10[1] = ord('e')
        t10[2] = ord('s')
        t10[3] = ord('t')
        t10[4] = ord(' ')
        t10[5] = ord('T')
        t10[6] = ord('1')
        t10[7] = ord('0')
        dd = bytearray(4)
        dd += t10
        dd[0] = 0x52  # iSCSI, ASCII
        dd[1] = 0xa1  # AssociatedWithTargetDevice, T10_VENDOR_ID
        dd[3] = len(t10)
        cmd.datain[pos:pos + len(dd)] = dd
        pos += len(dd)

        # Designation Descriptor: EUI-64, 8 byte version
        eui = bytearray(8)
        # IEEE company identifier
        eui[0] = 0x11
        eui[1] = 0x22
        eui[2] = 0x33
        # vendor specific
        eui[3] = ord('a')
        eui[4] = ord('b')
        eui[5] = ord('c')
        eui[6] = ord('d')
        eui[7] = ord('e')
        dd = bytearray(4)
        dd += eui
        dd[0] = 0x01  # BINARY
        dd[1] = 0x22  # AssociatedWithTargetDevice, EUI-64
        dd[2:4] = scsi_int_to_ba(len(t10), 2)
        cmd.datain[pos:pos + len(dd)] = dd
        pos += len(dd)

        cmd.datain[2:4] = scsi_int_to_ba(pos - 4, 2)


class MockReferrals(MockDevice):

    def execute(self, cmd):
        cmd.datain[0] = 0x00  # QUAL:0 TYPE:0
        cmd.datain[1] = 0xb3  # referrals
        cmd.datain[2] = 0x00  #
        cmd.datain[3] = 0x0c  # page length: 12
        cmd.datain[11] = 23
        cmd.datain[15] = 37


class MockExtendedInquiry(MockDevice):

    def execute(self, cmd):
        cmd.datain[0] = 0x00   # QUAL:0 TYPE:0
        cmd.datain[1] = 0x86   # extended inquiry
        cmd.datain[2] = 0x00   #
        cmd.datain[3] = 0x3c   # page length: 60
        cmd.datain[4] = 0x57   # activate microcode:1 spt:2 grd_chk:1
                               # app_chk:1 ref_chk:1
        cmd.datain[5] = 0x33   # uask_sup:1 group_sup:1 prior_sup:0 headsup:0
                           # ordsup:1 simpsup:1
        cmd.datain[6] = 0x05   # wu_sup:0 crd_sup:1 nv_sup:0 v_sup:1
        cmd.datain[7] = 0x11   # p_i_i_sup:1 luiclr:1
        cmd.datain[8] = 0x11   # r_sup:1 cbcs:1
        cmd.datain[9] = 0x03   # multi...:3
        cmd.datain[11] = 0x0f  # extended...:15
        cmd.datain[12] = 0xe0  # poa_sup:1 hra_sup:1 vsa_sup:1
        cmd.datain[13] = 0x05  # maximum...:5

class UnmarshallInquiryTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockInquiryStandard(sbc)) as s:
            cmd = s.inquiry()
            i = cmd.result
            self.assertEqual(i['peripheral_qualifier'], 1)
            self.assertEqual(i['peripheral_device_type'], 5)
            self.assertEqual(i['rmb'], 1)
            self.assertEqual(i['version'], 7)
            self.assertEqual(i['normaca'], 1)
            self.assertEqual(i['hisup'], 0)
            self.assertEqual(i['response_data_format'], 3)
            self.assertEqual(i['additional_length'], 64)
            self.assertEqual(i['sccs'], 1)
            self.assertEqual(i['acc'], 0)
            self.assertEqual(i['tpgs'], 3)
            self.assertEqual(i['3pc'], 1)
            self.assertEqual(i['protect'], 1)
            self.assertEqual(i['encserv'], 1)
            self.assertEqual(i['vs'], 1)
            self.assertEqual(i['multip'], 1)
            self.assertEqual(i['addr16'], 1)
            self.assertEqual(i['wbus16'], 1)
            self.assertEqual(i['sync'], 1)
            self.assertEqual(i['cmdque'], 1)
            self.assertEqual(i['vs2'], 1)
            self.assertEqual(i['clocking'], 2)
            self.assertEqual(i['qas'], 0)
            self.assertEqual(i['ius'], 1)
            self.assertEqual(i['t10_vendor_identification'].decode("utf-8"), 'abcdefgh')
            self.assertEqual(i['product_identification'].decode("utf-8"), 'iiiiiiiijjjjjjjj')
            self.assertEqual(i['product_revision_level'].decode("utf-8"), 'revn')

            d = Inquiry.unmarshall_datain(Inquiry.marshall_datain(i))
            self.assertEqual(d, i)

        with MockSCSI(MockLBP(sbc)) as s:
            cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.LOGICAL_BLOCK_PROVISIONING)
            i = cmd.result
            self.assertEqual(i['peripheral_qualifier'], 0)
            self.assertEqual(i['peripheral_qualifier'], 0)
            self.assertEqual(i['threshold_exponent'], 0x12)
            self.assertEqual(i['lbpu'], 1)
            self.assertEqual(i['lpbws'], 1)
            self.assertEqual(i['lbpws10'], 1)
            self.assertEqual(i['lbprz'], 1)
            self.assertEqual(i['anc_sup'], 1)
            self.assertEqual(i['dp'], 1)
            self.assertEqual(i['provisioning_type'], INQUIRY.PROVISIONING_TYPE.THIN_PROVISIONED)

            d = Inquiry.unmarshall_datain(Inquiry.marshall_datain(i), evpd=1)
            self.assertEqual(d, i)

        with MockSCSI(MockUSN(sbc)) as s:
            cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.UNIT_SERIAL_NUMBER)
            i = cmd.result
            self.assertEqual(i['peripheral_qualifier'], 0)
            self.assertEqual(i['peripheral_qualifier'], 0)
            self.assertEqual(i['unit_serial_number'].decode("utf-8"), "ABCD")

            d = Inquiry.unmarshall_datain(Inquiry.marshall_datain(i), evpd=1)
            self.assertEqual(d, i)

        with MockSCSI(MockReferrals(sbc)) as s:
            cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.REFERRALS)
            i = cmd.result
            self.assertEqual(i['peripheral_qualifier'], 0)
            self.assertEqual(i['peripheral_qualifier'], 0)
            self.assertEqual(i['user_data_segment_size'], 23)
            self.assertEqual(i['user_data_segment_multiplier'], 37)

            d = Inquiry.unmarshall_datain(Inquiry.marshall_datain(i), evpd=1)
            self.assertEqual(d, i)

        with MockSCSI(MockExtendedInquiry(sbc)) as s:
            cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.EXTENDED_INQUIRY_DATA)
            i = cmd.result
            self.assertEqual(i['peripheral_qualifier'], 0)
            self.assertEqual(i['peripheral_qualifier'], 0)
            self.assertEqual(i['activate_microcode'], 1)
            self.assertEqual(i['spt'], 2)
            self.assertEqual(i['grd_chk'], 1)
            self.assertEqual(i['app_chk'], 1)
            self.assertEqual(i['ref_chk'], 1)
            self.assertEqual(i['uask_sup'], 1)
            self.assertEqual(i['group_sup'], 1)
            self.assertEqual(i['prior_sup'], 0)
            self.assertEqual(i['headsup'], 0)
            self.assertEqual(i['ordsup'], 1)
            self.assertEqual(i['simpsup'], 1)
            self.assertEqual(i['wu_sup'], 0)
            self.assertEqual(i['crd_sup'], 1)
            self.assertEqual(i['nv_sup'], 0)
            self.assertEqual(i['v_sup'], 1)
            self.assertEqual(i['p_i_i_sup'], 1)
            self.assertEqual(i['luiclr'], 1)
            self.assertEqual(i['r_sup'], 1)
            self.assertEqual(i['cbcs'], 1)
            self.assertEqual(i['multi_it_nexus_microcode_download'], 3)
            self.assertEqual(i['extended_self_test_completion_minutes'], 15)
            self.assertEqual(i['poa_sup'], 1)
            self.assertEqual(i['hra_sup'], 1)
            self.assertEqual(i['vsa_sup'], 1)
            self.assertEqual(i['maximum_supported_sense_data_length'], 5)

            d = Inquiry.unmarshall_datain(Inquiry.marshall_datain(i), evpd=1)
            self.assertEqual(d, i)

            s.device = MockDevId(sbc)
            cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.DEVICE_IDENTIFICATION)
            i = cmd.result
            self.assertEqual(i['peripheral_qualifier'], 0)
            self.assertEqual(i['peripheral_qualifier'], 0)
            dd = i['designator_descriptors']
            self.assertEqual(len(dd), 2)
            # T10 designation descriptor
            self.assertEqual(dd[0]['association'], 2)
            self.assertEqual(dd[0]['code_set'], 2)
            self.assertEqual(dd[0]['designator_length'], 8)
            self.assertEqual(dd[0]['designator_type'], 1)
            self.assertEqual(dd[0]['piv'], 1)
            self.assertEqual(dd[0]['protocol_identifier'], 5)
            self.assertEqual(dd[0]['designator']['t10_vendor_id'].decode("utf-8"), 'Test T10')
            self.assertEqual(dd[0]['designator']['vendor_specific_id'].decode("utf-8"), '')
            # EUI-64 designation descriptor
            self.assertEqual(dd[1]['association'], 2)
            self.assertEqual(dd[1]['code_set'], 1)
            self.assertEqual(dd[1]['designator_length'], 8)
            self.assertEqual(dd[1]['designator_type'], 2)
            self.assertEqual(dd[1]['piv'], 0)
            self.assertFalse(hasattr(dd[1], 'protocol_identifier'))
            self.assertEqual(dd[1]['designator']['ieee_company_id'], 0x112233)
            self.assertEqual(dd[1]['designator']['vendor_specific_extension_id'].decode("utf-8"), 'abcde')

            d = Inquiry.unmarshall_datain(Inquiry.marshall_datain(i), evpd=1)
            self.assertEqual(d, i)
