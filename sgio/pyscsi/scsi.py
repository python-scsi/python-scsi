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

from scsi_device import SCSIDevice

from scsi_cdb_inquiry import Inquiry

class OPCODE:
    INQUIRY = 0x12

SCSI_STATUS_GOOD                 = 0x00
SCSI_STATUS_CHECK_CONDITION      = 0x02
SCSI_STATUS_CONDITIONS_MET       = 0x04
SCSI_STATUS_BUSY                 = 0x08
SCSI_STATUS_RESERVATION_CONFLICT = 0x18
SCSI_STATUS_TASK_SET_FULL        = 0x28
SCSI_STATUS_ACA_ACTIVE           = 0x30
SCSI_STATUS_TASK_ABORTED         = 0x40
SCSI_STATUS_SGIO_ERROR           = 0xff

class SCSI(SCSIDevice):
    '''

    '''
    def Inquiry(self, evpd = 0, page_code = 0, alloc_len = 96):
        '''

        :param evpd:
        :param page_code:
        :param alloc_len:
        :return:
        '''
        return Inquiry(self, evpd, page_code, alloc_len)

