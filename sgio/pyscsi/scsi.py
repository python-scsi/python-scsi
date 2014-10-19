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
from scsi_cdb_read10 import Read10
from scsi_cdb_read12 import Read12
from scsi_cdb_read16 import Read16
from scsi_cdb_readcapacity10 import ReadCapacity10
from scsi_cdb_readcapacity16 import ReadCapacity16
from scsi_cdb_testunitready import TestUnitReady
from scsi_cdb_write10 import Write10
from scsi_cdb_write12 import Write12
from scsi_cdb_write16 import Write16


class SCSI(object):
    """
    The interface to  the specialized scsi classes
    """
    def __init__(self, dev):
        self.device = dev
        self._blocksize = 0

    @property
    def blocksize(self):
        """
        getter method of the blocksize property

        :return blocksize in bytes
        """
        return self._blocksize

    @blocksize.setter
    def blocksize(self, value):
        """
        setter method of the blocksize property

        :param blocksize in bytes
        """
        self._blocksize = value

    def inquiry(self, evpd=0, page_code=0, alloc_len=96):
        """
        Returns a Inquiry Instance

        :param evpd: a byte indicating if vital product data is supported
        :param page_code: a byte representing a page code for vpd
        :param alloc_len: a integer , the size of the data_in buffer
        :return: a Inquiry instance
        """
        return Inquiry(self, evpd, page_code, alloc_len)

    def read10(self, lba, tl, **kwargs):
        """
        Returns a Read10 Instance

        :lba Logical Block Address
        :tl Transfer Length
        :rdprotect ReadProtect
        :dpo DPO
        :fua FUA
        :rarc RARC
        :group Group Number
        """
        return Read10(self, lba, tl, **kwargs)

    def read12(self, lba, tl, **kwargs):
        """
        Returns a Read12 Instance

        :lba Logical Block Address
        :tl Transfer Length
        :rdprotect ReadProtect
        :dpo DPO
        :fua FUA
        :rarc RARC
        :group Group Number
        """
        return Read12(self, lba, tl, **kwargs)

    def read16(self, lba, tl, **kwargs):
        """
        Returns a Read16 Instance

        :lba Logical Block Address
        :tl Transfer Length
        :rdprotect ReadProtect
        :dpo DPO
        :fua FUA
        :rarc RARC
        :group Group Number
        """
        return Read16(self, lba, tl, **kwargs)

    def readcapacity10(self, alloc_len=8):
        """
        Returns a ReadCapacity10 Instance

        :param alloc_len: a integer , the size of the data_in buffer
        :return: a ReadCapacity10 instance
        """
        return ReadCapacity10(self, alloc_len)

    def readcapacity16(self, alloc_len=32):
        """
        Returns a ReadCapacity16 Instance

        :param alloc_len: a integer , the size of the data_in buffer
        :return: a ReadCapacity16 instance
        """
        return ReadCapacity16(self, alloc_len)

    def testunitready(self):
        """
        Returns a TestUnitReady Instance

        No params
        No return value
        """
        return TestUnitReady(self)

    def write10(self, lba, tl, data, **kwargs):
        """
        Returns a Write10 Instance

        :lba Logical Block Address
        :tl Transfer Length
        :data bytearray containing the data to write
        :wrprotect WriteProtect
        :dpo DPO
        :fua FUA
        :group Group Number
        """
        return Write10(self, lba, tl, data, **kwargs)

    def write12(self, lba, tl, data, **kwargs):
        """
        Returns a Write12 Instance

        :lba Logical Block Address
        :tl Transfer Length
        :data bytearray containing the data to write
        :wrprotect WriteProtect
        :dpo DPO
        :fua FUA
        :group Group Number
        """
        return Write12(self, lba, tl, data, **kwargs)

    def write16(self, lba, tl, data, **kwargs):
        """
        Returns a Write16 Instance

        :lba Logical Block Address
        :tl Transfer Length
        :data bytearray containing the data to write
        :wrprotect WriteProtect
        :dpo DPO
        :fua FUA
        :group Group Number
        """
        return Write16(self, lba, tl, data, **kwargs)

