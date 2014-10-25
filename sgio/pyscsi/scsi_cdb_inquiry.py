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

from scsi_command import SCSICommand, OPCODE
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
        decode_bits(cdb, inquiry_enums.cdb_bits, _tmp)
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
            self.result.update({'t10_vendor_identification': self.datain[8:16]})
            self.result.update({'product_identification': self.datain[16:32]})
            self.result.update({'product_revision_level': self.datain[32:36]})
            decode_bits(self.datain, inquiry_enums.inq_std_bits, self.result)
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
            decode_bits(self.datain, inquiry_enums.inq_blocklimits_bits, self.result)

        if self._page_code == inquiry_enums.VPD.BLOCK_DEVICE_CHARACTERISTICS:
            decode_bits(self.datain, inquiry_enums.inq_blockdevchar_bits, self.result)

        if self._page_code == inquiry_enums.VPD.LOGICAL_BLOCK_PROVISIONING:
            decode_bits(self.datain, inquiry_enums.inq_logicalblockprov_bits, self.result)

        if self._page_code == inquiry_enums.VPD.UNIT_SERIAL_NUMBER:
            self.result.update({'unit_serial_number': self.datain[4:4 + page_length]})
