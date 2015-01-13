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
from pyscsi.utils.converter import decode_bits
import scsi_enum_modesense6 as modesensense_enums

#
# SCSI ModeSense6 command and definitions
#


class ModeSense6(SCSICommand):
    """
    A class to hold information from a moesense6 command
    """

    def __init__(self, scsi, page_code, sub_page_code=0, dbd=0, pc=0,
                 alloclen=96):
        """
        initialize a new instance

        :param scsi: a SCSI instance
        :param page_code: the page code for the vpd page
        :param sub_page_code:
        :param dbd:
        :param pc:
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self, scsi, 0, alloclen)
        self.page_code = page_code
        self.sub_page_code = sub_page_code
        self.cdb = self.build_cdb(self.page_code, self.sub_page_code, dbd, pc,
                                  alloclen)
        self.execute()

    def build_cdb(self, page_code, sub_page_code, dbd, pc, alloclen):
        """
        """
        cdb = self.init_cdb(self.scsi.device.opcodes.MODE_SENSE_6.value)
        if dbd:
            cdb[1] |= 0x08
        cdb[2] |= (pc << 6) & 0xc0
        cdb[2] |= page_code & 0x3f
        cdb[3] = sub_page_code
        cdb[4] = alloclen
        return cdb

    def unmarshall_cdb(self, cdb):
        """
        method to unmarshall a byte array containing a cdb.
        """
        _tmp = {}
        _bits = {'opcode': [0xff, 0],
                 'dbd': [0x08, 1],
                 'pc': [0xc0, 2],
                 'page_code': [0x3f, 2],
                 'sub_page_code': [0xff, 3],
                 'alloc_len': [0xff, 4], }
        decode_bits(cdb, _bits, _tmp)
        return _tmp

    def unmarshall(self):
        """
        """
        _bits = {'mode_data_length': [0xff, 0],
                 'medium_type': [0xff, 1],
                 'device_specific_parameter': [0xff, 2],
                 'block_descriptor_length': [0xff, 3], }
        decode_bits(self.datain[0:4], _bits, self.result)
        _bdl = self.result['block_descriptor_length']

        block_descriptor = self.datain[4:]
        
        mode_data = block_descriptor[_bdl:]
        _bits = {'ps': [0x80, 0],
                 'spf': [0x40, 0],
                 'page_code': [0x3f, 0],
                 'parameter_list_length': [0xff, 1], }
        decode_bits(mode_data, _bits, self.result)

        if self.page_code == modesensense_enums.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT:
            _bits = {'first_medium_transport_element_address': [0xffff, 2],
                     'num_medium_transport_elements': [0xffff, 4],
                     'first_storage_element_address': [0xffff, 6],
                     'num_storage_elements': [0xffff, 8],
                     'first_import_element_address': [0xffff, 10],
                     'num_import_elements': [0xffff, 12],
                     'first_data_transfer_element_address': [0xffff, 14],
                     'num_data_transfer_elements': [0xffff, 16], }
            decode_bits(mode_data, _bits, self.result)
