#!/usr/bin/env python
# coding: utf-8
from .mock_device import MockDevice, MockSCSI
from pyscsi.utils.converter import scsi_int_to_ba
from pyscsi.pyscsi.scsi_enum_command import sbc
from pyscsi.pyscsi import scsi_enum_inquiry as INQUIRY
from pyscsi.pyscsi.scsi_cdb_inquiry import Inquiry


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


def main():
    with MockSCSI(MockInquiryStandard(sbc)) as s:
        cmd = s.inquiry()
        i = cmd.result
        assert i['peripheral_qualifier'] == 1
        assert i['peripheral_device_type'] == 5
        assert i['rmb'] == 1
        assert i['version'] == 7
        assert i['normaca'] == 1
        assert i['hisup'] == 0
        assert i['response_data_format'] == 3
        assert i['additional_length'] == 64
        assert i['sccs'] == 1
        assert i['acc'] == 0
        assert i['tpgs'] == 3
        assert i['3pc'] == 1
        assert i['protect'] == 1
        assert i['encserv'] == 1
        assert i['vs'] == 1
        assert i['multip'] == 1
        assert i['addr16'] == 1
        assert i['wbus16'] == 1
        assert i['sync'] == 1
        assert i['cmdque'] == 1
        assert i['vs2'] == 1
        assert i['clocking'] == 2
        assert i['qas'] == 0
        assert i['ius'] == 1
        assert i['t10_vendor_identification'].decode("utf-8") == 'abcdefgh'
        assert i['product_identification'].decode("utf-8") == 'iiiiiiiijjjjjjjj'
        assert i['product_revision_level'].decode("utf-8") == 'revn'

        d = Inquiry.unmarshall_datain(Inquiry.marshall_datain(i))
        assert d == i

    with MockSCSI(MockLBP(sbc)) as s:
        cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.LOGICAL_BLOCK_PROVISIONING)
        i = cmd.result
        assert i['peripheral_qualifier'] == 0
        assert i['peripheral_qualifier'] == 0
        assert i['threshold_exponent'] == 0x12
        assert i['lbpu'] == 1
        assert i['lpbws'] == 1
        assert i['lbpws10'] == 1
        assert i['lbprz'] == 1
        assert i['anc_sup'] == 1
        assert i['dp'] == 1
        assert i['provisioning_type'] == INQUIRY.PROVISIONING_TYPE.THIN_PROVISIONED

        d = Inquiry.unmarshall_datain(Inquiry.marshall_datain(i), evpd=1)
        assert d == i

    with MockSCSI(MockUSN(sbc)) as s:
        cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.UNIT_SERIAL_NUMBER)
        i = cmd.result
        assert i['peripheral_qualifier'] == 0
        assert i['peripheral_qualifier'] == 0
        assert i['unit_serial_number'].decode("utf-8") == "ABCD"

        d = Inquiry.unmarshall_datain(Inquiry.marshall_datain(i), evpd=1)
        assert d == i

    with MockSCSI(MockReferrals(sbc)) as s:
        cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.REFERRALS)
        i = cmd.result
        assert i['peripheral_qualifier'] == 0
        assert i['peripheral_qualifier'] == 0
        assert i['user_data_segment_size'] == 23
        assert i['user_data_segment_multiplier'] == 37

        d = Inquiry.unmarshall_datain(Inquiry.marshall_datain(i), evpd=1)
        assert d == i

    with MockSCSI(MockExtendedInquiry(sbc)) as s:
        cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.EXTENDED_INQUIRY_DATA)
        i = cmd.result
        assert i['peripheral_qualifier'] == 0
        assert i['peripheral_qualifier'] == 0
        assert i['activate_microcode'] == 1
        assert i['spt'] == 2
        assert i['grd_chk'] == 1
        assert i['app_chk'] == 1
        assert i['ref_chk'] == 1
        assert i['uask_sup'] == 1
        assert i['group_sup'] == 1
        assert i['prior_sup'] == 0
        assert i['headsup'] == 0
        assert i['ordsup'] == 1
        assert i['simpsup'] == 1
        assert i['wu_sup'] == 0
        assert i['crd_sup'] == 1
        assert i['nv_sup'] == 0
        assert i['v_sup'] == 1
        assert i['p_i_i_sup'] == 1
        assert i['luiclr'] == 1
        assert i['r_sup'] == 1
        assert i['cbcs'] == 1
        assert i['multi_it_nexus_microcode_download'] == 3
        assert i['extended_self_test_completion_minutes'] == 15
        assert i['poa_sup'] == 1
        assert i['hra_sup'] == 1
        assert i['vsa_sup'] == 1
        assert i['maximum_supported_sense_data_length'] == 5

        d = Inquiry.unmarshall_datain(Inquiry.marshall_datain(i), evpd=1)
        assert d == i

        s.device = MockDevId(sbc)
        cmd = s.inquiry(evpd=1, page_code=INQUIRY.VPD.DEVICE_IDENTIFICATION)
        i = cmd.result
        assert i['peripheral_qualifier'] == 0
        assert i['peripheral_qualifier'] == 0
        dd = i['designator_descriptors']
        assert len(dd) == 2
        # T10 designation descriptor
        assert dd[0]['association'] == 2
        assert dd[0]['code_set'] == 2
        assert dd[0]['designator_length'] == 8
        assert dd[0]['designator_type'] == 1
        assert dd[0]['piv'] == 1
        assert dd[0]['protocol_identifier'] == 5
        assert dd[0]['designator']['t10_vendor_id'].decode("utf-8") == 'Test T10'
        assert dd[0]['designator']['vendor_specific_id'].decode("utf-8") == ''
        # EUI-64 designation descriptor
        assert dd[1]['association'] == 2
        assert dd[1]['code_set'] == 1
        assert dd[1]['designator_length'] == 8
        assert dd[1]['designator_type'] == 2
        assert dd[1]['piv'] == 0
        assert not hasattr(dd[1], 'protocol_identifier')
        assert dd[1]['designator']['ieee_company_id'] == 0x112233
        assert dd[1]['designator']['vendor_specific_extension_id'].decode("utf-8") == 'abcde'

        d = Inquiry.unmarshall_datain(Inquiry.marshall_datain(i), evpd=1)
        assert d == i


if __name__ == "__main__":
    main()

