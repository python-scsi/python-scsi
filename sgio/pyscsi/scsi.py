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


class SCSI(SCSIDevice):
    """
    The interface to  the specialized scsi classes
    """
    def inquiry(self, evpd=0, page_code=0, alloc_len=96):
        """
        Returns a Inquiry Instance

        :param evpd: a byte indicating if vital product data is supported
        :param page_code: a byte representing a page code for vpd
        :param alloc_len: a integer , the size of the data_in buffer
        :return: a Inquiry instance
        """
        return Inquiry(self, evpd, page_code, alloc_len)