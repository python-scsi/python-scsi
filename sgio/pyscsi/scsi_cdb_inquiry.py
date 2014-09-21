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
from sgio.utils.converter import scsi_16_to_ba
#
# SCSI Inquiry command and definitions
#

#
# INQUIRY VPD pages
#


class VPD(object):
    """
    A class to act as a fake enumerator for vital product data page codes
    """
    SUPPORTED_VPD_PAGES = 0x00
    DEVICE_IDENTIFICATION = 0x83


class Inquiry(SCSICommand):
    """
    A class to hold information from a inquiry command to a scsi device
    """

    def __init__(self, dev, evpd=0, page_code=0, alloclen=96):
        """
        initialize a new instance

        :param dev: a SCSIDevice instance
        :param evpd: the byte to enable or disable vital product data
        :param page_code: the page code for the vpd page
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        self.device = dev
        SCSICommand.__init__(self, self.device, 0, alloclen)
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
        cdb[3:5] = scsi_16_to_ba(alloclen)
        return cdb

    def unmarshall(self):
        """
        method to extract relevant data from the byte array that the inquiry command returns

        the content of the result dict depends if vital product data is enabled or not. if vpd is
        enabled we create a list with the received vpd.
        """
        if self._evpd == 0:
            self.add_result('peripheral_qualifier', self.datain[0] >> 5)
            self.add_result('peripheral_qualifier', self.datain[0] >> 5)
            self.add_result('peripheral_device_type', self.datain[0] & 0x1f)
            self.add_result('version', self.datain[2])
            self.add_result('normaca', self.datain[3] & 0x20)
            self.add_result('hisup', self.datain[3] & 0x10)
            self.add_result('response_data_format', self.datain[3] & 0x0f)
            self.add_result('additional_length', self.datain[4])
            self.add_result('sccs', self.datain[5] & 0x80)
            self.add_result('acc', self.datain[5] & 0x40)
            self.add_result('tpgs', (self.datain[5] >> 4) & 0x03)
            self.add_result('3pc', self.datain[5] & 0x08)
            self.add_result('protect', self.datain[5] & 0x01)
            self.add_result('encserv', self.datain[6] & 0x40)
            self.add_result('vs', self.datain[6] & 0x20)
            self.add_result('multip', self.datain[6] & 0x10)
            self.add_result('addr16', self.datain[6] & 0x01)
            self.add_result('wbus16', self.datain[7] & 0x20)
            self.add_result('sync', self.datain[7] & 0x10)
            self.add_result('cmdque', self.datain[7] & 0x02)
            self.add_result('vs2', self.datain[7] & 0x01)
            self.add_result('t10_vendor_identification', self.datain[8:16])
            self.add_result('product_identification', self.datain[16:32])
            self.add_result('product_revision_level', self.datain[32:36])
            self.add_result('clocking', (self.datain[56] >> 2) & 0x03)
            self.add_result('qas', self.datain[56] & 0x02)
            self.add_result('ius', self.datain[56] & 0x01)
        elif self._page_code == VPD.SUPPORTED_VPD_PAGES:
            self.add_result('peripheral_qualifier', self.datain[0] >> 5)
            self.add_result('peripheral_device_type', self.datain[0] & 0x1f)
            self.add_result('page_code', self.datain[1])
            page_length = self.datain[2] * 256 + self.datain[3]
            self.add_result('page_length', page_length)

            vpd_pages = []
            for i in range(page_length):
                vpd_pages.append(self.datain[i + 4])
                self.add_result('vpd_pages', vpd_pages )
