# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE
from pyscsi.utils.converter import scsi_int_to_ba, scsi_ba_to_int, decode_bits
import scsi_enum_inquiry as inquiry_enums

#
# SCSI Inquiry command and definitions
#


class Inquiry(SCSICommand):
    """
    A class to hold information from a inquiry command to a scsi device
    """

    def __init__(self, scsi, evpd=0, page_code=0, alloclen=96):
        """
        initialize a new instance

        :param scsi: a SCSI instance
        :param evpd: the byte to enable or disable vital product data
        :param page_code: the page code for the vpd page
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self, scsi, 0, alloclen)
        self._evpd = evpd
        self.pagecode = page_code
        self.cdb = self.build_cdb(evpd, self.pagecode, alloclen)
        self.execute()

    def build_cdb(self, evpd, page_code, alloclen):
        """
        method to create a byte array for a Command Descriptor Block with a proper length

        init_cdb returns a byte array of 6,10,12 or 16 bytes depending on the operation code and if
        vital product data is enabled

        :param evpd: the byte to enable or disable vital product data
        :param page_code: the page code for the vpd page
        :param alloclen: the max number of bytes allocated for the data_in buffer
        :return: a byte array representing a code descriptor block
        """
        cdb = SCSICommand.init_cdb(OPCODE.INQUIRY)
        if evpd:
            cdb[1] |= 0x01
            cdb[2] = page_code
        cdb[3:5] = scsi_int_to_ba(alloclen, 2)
        return cdb

    def unmarshall_cdb(self, cdb):
        """
        method to unmarshall a byte array containing a cdb.
        """
        _tmp = {}
        _bits = {'opcode': [0xff, 0],
                 'evpd': [0x01, 1],
                 'page_code': [0xff, 2],
                 'alloc_len': [0xffff, 3], }
        decode_bits(cdb, _bits, _tmp)
        return _tmp

    def unmarshall_designator(self, type, data):
        _d = {}
        if type == inquiry_enums.DESIGNATOR.VENDOR_SPECIFIC:
            _d['vendor_specific'] = data

        if type == inquiry_enums.DESIGNATOR.T10_VENDOR_ID:
            _d['t10_vendor_id'] = data[:8]
            _d['vendor_specific_id'] = data[8:]

        if type == inquiry_enums.DESIGNATOR.EUI_64:
            if len(data) == 8:
                _d['ieee_company_id'] = scsi_ba_to_int(data[:3])
                _d['vendor_specific_extension_id'] = data[3:8]
            if len(data) == 12:
                _d['ieee_company_id'] = scsi_ba_to_int(data[:3])
                _d['vendor_specific_extension_id'] = data[3:8]
                _d['directory_id'] = data[8:]
            if len(data) == 16:
                _d['identifier_extension'] = data[:8]
                _d['ieee_company_id'] = scsi_ba_to_int(data[8:11])
                _d['vendor_specific_extension_id'] = data[11:]

        if type == inquiry_enums.DESIGNATOR.NAA:
            _d['naa'] = data[0] >> 4
            if _d['naa'] == inquiry_enums.NAA.IEEE_EXTENDED:
                _bits = {'vendor_specific_identifier_a': [0x0fff, 0],
                         'ieee_company_id': [0xffffff, 2],
                         'vendor_specific_identifier_b': [0xffffff, 5], }
                decode_bits(data, _bits, _d)
            if _d['naa'] == inquiry_enums.NAA.LOCALLY_ASSIGNED:
                _d['locally_administered_value'] = data[0:8]
            if _d['naa'] == inquiry_enums.NAA.IEEE_REGISTERED:
                _bits = {'ieee_company_id': [0x0ffffff0, 0],
                         'vendor_specific_identifier': [0x0fffffffff, 3], }
                decode_bits(data, _bits, _d)
            if _d['naa'] == inquiry_enums.NAA.IEEE_REGISTERED_EXTENDED:
                _bits = {'ieee_company_id': [0x0ffffff0, 0],
                         'vendor_specific_identifier': [0x0fffffffff, 3],
                         'vendor_specific_identifier_extension': [0xffffffffffffffff, 8], }
                decode_bits(data, _bits, _d)

        if type == inquiry_enums.DESIGNATOR.RELATIVE_TARGET_PORT_IDENTIFIER:
                _bits = {'relative_port': [0xffff, 2], }
                decode_bits(data, _bits, _d)

        if type == inquiry_enums.DESIGNATOR.TARGET_PORTAL_GROUP:
                _bits = {'target_portal_group': [0xffff, 2], }
                decode_bits(data, _bits, _d)

        if type == inquiry_enums.DESIGNATOR.LOGICAL_UNIT_GROUP:
                _bits = {'logical_unit_group': [0xffff, 2], }
                decode_bits(data, _bits, _d)

        if type == inquiry_enums.DESIGNATOR.MD5_LOGICAL_IDENTIFIER:
                _d['md5_logical_identifier'] = data[0:16]

        if type == inquiry_enums.DESIGNATOR.SCSI_NAME_STRING:
                _d['scsi_name_string'] = data

        if type == inquiry_enums.DESIGNATOR.PCI_EXPRESS_ROUTING_ID:
                _bits = {
                    'pci_express_routing_id': [0xffff, 0],
                }
                decode_bits(data, _bits, _d)

        return _d

    def unmarshall_designator_descriptor(self, data):
        _bits = {
            'protocol_identifier': [0xf0, 0],
            'code_set': [0x0f, 0],
            'piv': [0x80, 1],
            'association': [0x30, 1],
            'designator_type': [0x0f, 1],
            'designator_length': [0xff, 3],
            }
        _d = {}
        decode_bits(data, _bits, _d)
        if _d['piv'] == 0 or (_d['association'] != 1 and _d['association'] != 2):
            del _d['protocol_identifier']
        _d['designator'] = self.unmarshall_designator(_d['designator_type'], data[4:])
        return _d

    def unmarshall(self):
        """
        method to extract relevant data from the byte array that the inquiry command returns

        the content of the result dict depends if vital product data is enabled or not. if vpd is
        enabled we create a list with the received vpd.
        """
        self.result.update({'peripheral_qualifier': self.datain[0] >> 5})
        self.result.update({'peripheral_device_type': self.datain[0] & 0x1f})
        if self._evpd == 0:
            _bits = {'rmb': [0x80, 1],
                     'version': [0xff, 2],
                     'normaca': [0x20, 3],
                     'hisup': [0x10, 3],
                     'response_data_format': [0x0f, 3],
                     'additional_length': [0xff, 4],
                     'sccs': [0x80, 5],
                     'acc': [0x40, 5],
                     'tpgs': [0x30, 5],
                     '3pc': [0x08, 5],
                     'protect': [0x01, 5],
                     'encserv': [0x40, 6],
                     'vs': [0x20, 6],
                     'multip': [0x10, 6],
                     'addr16': [0x01, 6],
                     'wbus16': [0x20, 7],
                     'sync': [0x10, 7],
                     'cmdque': [0x02, 7],
                     'vs2': [0x01, 7],
                     'clocking': [0x0c, 56],
                     'qas': [0x02, 56],
                     'ius': [0x01, 56], }
            self.result.update({'t10_vendor_identification': self.datain[8:16]})
            self.result.update({'product_identification': self.datain[16:32]})
            self.result.update({'product_revision_level': self.datain[32:36]})
            decode_bits(self.datain, _bits, self.result)
            return

        self.result.update({'page_code': self.datain[1]})
        page_length = scsi_ba_to_int(self.datain[2:4])
        self.result.update({'page_length': page_length})

        if self._page_code == inquiry_enums.VPD.SUPPORTED_VPD_PAGES:
            vpd_pages = []
            for i in range(page_length):
                vpd_pages.append(self.datain[i + 4])
                self.result.update({'vpd_pages': vpd_pages})

        if self._page_code == inquiry_enums.VPD.BLOCK_LIMITS:
            _bits = {'wsnz': [0x01, 4],
                     'ugavalid': [0x80, 32],
                     'max_caw_len': [0xff, 5],
                     'opt_xfer_len_gran': [0xffff, 6],
                     'max_xfer_len': [0xffffffff, 8],
                     'opt_xfer_len': [0xffffffff, 12],
                     'max_pfetch_len': [0xffffffff, 16],
                     'max_unmap_lba_count': [0xffffffff, 20],
                     'max_unmap_bd_count': [0xffffffff, 24],
                     'opt_unmap_gran': [0xffffffff, 28],
                     'unmap_gran_alignment': [0xffffffff, 32],
                     'max_ws_len': [0xffffffff, 36], }
            decode_bits(self.datain, _bits, self.result)

        if self._page_code == inquiry_enums.VPD.BLOCK_DEVICE_CHARACTERISTICS:
            _bits = {'wabereq': [0xc0, 7],
                     'wacereq': [0x30, 7],
                     'nominal_form_factor': [0x0f, 7],
                     'fuab': [0x02, 8],
                     'vbuls': [0x01, 8],
                     'medium_rotation_rate': [0xffff, 4],
                     'product_type': [0xff, 6], }
            decode_bits(self.datain, _bits, self.result)

        if self._page_code == inquiry_enums.VPD.LOGICAL_BLOCK_PROVISIONING:
            _bits = {'threshold_exponent': [0xff, 4],
                     'lbpu': [0x80, 5],
                     'lpbws': [0x40, 5],
                     'lbpws10': [0x20, 5],
                     'lbprz': [0x04, 5],
                     'anc_sup': [0x02, 5],
                     'dp': [0x01, 5],
                     'provisioning_type': [0x07, 6], }
            decode_bits(self.datain, _bits, self.result)

        if self._page_code == inquiry_enums.VPD.REFERRALS:
            _bits = {'user_data_segment_size': [0xffffffff, 8],
                     'user_data_segment_multiplier': [0xffffffff, 12], }
            decode_bits(self.datain, _bits, self.result)

        if self._page_code == inquiry_enums.VPD.UNIT_SERIAL_NUMBER:
            self.result.update({'unit_serial_number': self.datain[4:4 + page_length]})

        if self._page_code == inquiry_enums.VPD.EXTENDED_INQUIRY_DATA:
            _bits = {'activate_microcode': [0xc0, 4],
                     'spt': [0x38, 4],
                     'grd_chk': [0x04, 4],
                     'app_chk': [0x02, 4],
                     'ref_chk': [0x01, 4],
                     'uask_sup': [0x20, 5],
                     'group_sup': [0x10, 5],
                     'prior_sup': [0x08, 5],
                     'headsup': [0x04, 5],
                     'ordsup': [0x02, 5],
                     'simpsup': [0x01, 5],
                     'wu_sup': [0x08, 6],
                     'crd_sup': [0x04, 6],
                     'nv_sup': [0x02, 6],
                     'v_sup': [0x01, 6],
                     'p_i_i_sup': [0x10, 7],
                     'luiclr': [0x01, 7],
                     'r_sup': [0x10, 8],
                     'cbcs': [0x01, 8],
                     'multi_it_nexus_microcode_download': [0x0f, 9],
                     'extended_self_test_completion_minutes': [0xffff, 10],
                     'poa_sup': [0x80, 12],
                     'hra_sup': [0x40, 12],
                     'vsa_sup': [0x20, 12],
                     'maximum_supported_sense_data_length': [0xff, 13], }
            decode_bits(self.datain, _bits, self.result)

        if self._page_code == inquiry_enums.VPD.DEVICE_IDENTIFICATION:
            _data = self.datain[4:4 + page_length]
            _d = []
            while len(_data):
                _bytes = _data[3] + 4
                _d.append(self.unmarshall_designator_descriptor(_data[:_bytes]))
                _data = _data[_bytes:]

            self.result.update({'designator_descriptors': _d})
