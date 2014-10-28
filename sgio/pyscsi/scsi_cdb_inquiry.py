# coding: utf-8


#      Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
#
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU Lesser General Public License as published by
#	   the Free Software Foundation; either version 2.1 of the License, or
#	   (at your option) any later version.
#
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU Lesser General Public License for more details.
#
#	   You should have received a copy of the GNU Lesser General Public License
#	   along with this program; if not, see <http://www.gnu.org/licenses/>.

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE
from sgio.utils.converter import scsi_int_to_ba, scsi_ba_to_int, decode_bits
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

        if self._page_code == inquiry_enums.VPD.UNIT_SERIAL_NUMBER:
            self.result.update({'unit_serial_number': self.datain[4:4 + page_length]})
