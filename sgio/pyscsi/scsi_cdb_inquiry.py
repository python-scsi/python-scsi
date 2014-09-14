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

#
# SCSI Inquiry command and definitions
#
SCSI_CDB_INQUIRY = 0x12

#
# INQUIRY VPD pages
#
class VPD:
    SUPPORTED_VPD_PAGES   = 0x00
    DEVICE_IDENTIFICATION = 0x83

class Inquiry(SCSICommand):
    '''

    '''
    def __init__(self, dev, evpd = 0, page_code = 0, alloclen = 96):
        '''

        :param dev:
        :param evpd:
        :param page_code:
        :param alloclen:
        :return:
        '''
        self._evpd = evpd
        self._page_code = page_code
        SCSICommand.__init__(self, dev, 0, alloclen)
        self.cdb = self.build_cdb(evpd, page_code, alloclen)
        self.execute()

    def build_cdb(self, evpd, page_code, alloclen ):
        '''

        :param evpd:
        :param page_code:
        :param alloclen:
        :return:
        '''
        cdb = bytearray([SCSI_CDB_INQUIRY, 0x00, 0x00, 0x00, 0x00, 0x00])
        if (evpd):
            cdb[1] |= 0x01
            cdb[2] = page_code
        cdb[3] = alloclen >> 8
        cdb[4] = alloclen & 0xff
        return cdb

    def unmarshall(self):
        '''

        :return:
        '''
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
            return
        if self._page_code == VPD.SUPPORTED_VPD_PAGES:
            self.add_result('peripheral_qualifier', self.datain[0] >> 5)
            self.add_result('peripheral_device_type', self.datain[0] & 0x1f)
            self.add_result('page_code', self.datain[1])
            page_length = self.datain[2] * 256 + self.datain[3]
            self.add_result('page_length', page_length )

            vpd_pages = []
            for i in range(page_length):
                vpd_pages.append(self.datain[i + 4])
                self.add_result('vpd_pages', vpd_pages )
            return
