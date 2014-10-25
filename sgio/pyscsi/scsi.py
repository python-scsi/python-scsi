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

from scsi_cdb_inquiry import Inquiry
from scsi_cdb_modesense6 import ModeSense6
from scsi_cdb_read10 import Read10
from scsi_cdb_read12 import Read12
from scsi_cdb_read16 import Read16
from scsi_cdb_readcapacity10 import ReadCapacity10
from scsi_cdb_readcapacity16 import ReadCapacity16
from scsi_cdb_readelementstatus import ReadElementStatus
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

        :return: blocksize in bytes
        """
        return self._blocksize

    @blocksize.setter
    def blocksize(self, value):
        """
        setter method of the blocksize property

        :param: blocksize in bytes
        """
        self._blocksize = value

    def inquiry(self, **kwargs):
        """
        Returns a Inquiry Instance

        :param evpd = 0: a byte indicating if vital product data is supported
        :param page_code = 0: a byte representing a page code for vpd
        :param alloc_len = 96: a integer , the size of the data_in buffer
        :return: a Inquiry instance
        """
        return Inquiry(self, **kwargs)

    def modesense6(self, page_code, **kwargs):
        """
        Returns a ModeSense6 Instance

        :param page_code:  The page requested
        :param sub_page_code = 0: Requested subpage
        :param dbd = 0: Disable Block Descriptors flag
        :param pc = 0: Page Control flag
        :param alloclen = 96
        :return: a ModeSense6 instance
        """
        return ModeSense6(self, page_code, **kwargs)

    def read10(self, lba, tl, **kwargs):
        """
        Returns a Read10 Instance

        :param lba: Logical Block Address
        :param tl: Transfer Length
        :param rdprotect = 0: ReadProtect flags
        :param dpo = 0: DisablePageOut flag
        :param fua = 0: Force Unit Access flag 
        :param rarc = 0: Rebuild Assist Recovery control flag
        :param group = 0: Group Number
        :returns the data returned in self.datain
        """
        return Read10(self, lba, tl, **kwargs)

    def read12(self, lba, tl, **kwargs):
        """
        Returns a Read12 Instance

        :param lba: Logical Block Address
        :param tl: Transfer Length
        :param rdprotect = 0: ReadProtect flags
        :param dpo = 0: DisablePageOut flag
        :param fua = 0: Force Unit Access flag 
        :param rarc = 0: Rebuild Assist Recovery control flag
        :param group = 0: Group Number
        :returns the data returned in self.datain
        """
        return Read12(self, lba, tl, **kwargs)

    def read16(self, lba, tl, **kwargs):
        """
        Returns a Read16 Instance

        :param lba: Logical Block Address
        :param tl: Transfer Length
        :param rdprotect = 0: ReadProtect flags
        :param dpo = 0: DisablePageOut flag
        :param fua = 0: Force Unit Access flag 
        :param rarc = 0: Rebuild Assist Recovery control flag
        :param group = 0: Group Number
        :returns the data returned in self.datain
        """
        return Read16(self, lba, tl, **kwargs)

    def readcapacity10(self, **kwargs):
        """
        Returns a ReadCapacity10 Instance

        :param alloc_len = 8: size of requested datain
        :return: a ReadCapacity10 instance
        """
        return ReadCapacity10(self, **kwargs)

    def readcapacity16(self, **kwargs):
        """
        Returns a ReadCapacity16 Instance

        :param alloc_len = 32: size of requested datain
        :return: a ReadCapacity16 instance
        """
        return ReadCapacity16(self, **kwargs)

    def readelementstatus(self, start, num, **kwargs):
        """
        Returns a ReadElementStatus Instance

        :param start: starting address for first element to return
        :param num: numbver of elements to return
        :param element_type=ELEMENT_TYPE.ALL: type of elements to return
        :param voltag = 0: whether volume tag data should be returned
        :param curdata = 1: check current data
        :param dvcid = 0: whether to return device identifiers
        :param alloclen=16384: max amount od data to return
        :return: an ReadElementStatus instance
        """
        return ReadElementStatus(self, start, num, **kwargs)

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

        :param lba: Logical Block Address to write to
        :param tl: Transfer Length in blocks
        :param data: bytearray containing the data to write
        :param wrprotect = 0: WriteProtect flags
        :param dpo = 0: disable Page Out flag
        :param fua = 0: Force Unit Access flag
        :param group = 0: Group Number
        :return: a Write10 instance
        """
        return Write10(self, lba, tl, data, **kwargs)

    def write12(self, lba, tl, data, **kwargs):
        """
        Returns a Write12 Instance

        :param lba: Logical Block Address to write to
        :param tl: Transfer Length in blocks
        :param data: bytearray containing the data to write
        :param wrprotect = 0: WriteProtect flags
        :param dpo = 0: disable Page Out flag
        :param fua = 0: Force Unit Access flag
        :param group = 0: Group Number
        :return: a Write12 instance
        """
        return Write12(self, lba, tl, data, **kwargs)

    def write16(self, lba, tl, data, **kwargs):
        """
        Returns a Write16 Instance

        :param lba: Logical Block Address to write to
        :param tl: Transfer Length in blocks
        :param data: bytearray containing the data to write
        :param wrprotect = 0: WriteProtect flags
        :param dpo = 0: disable Page Out flag
        :param fua = 0: Force Unit Access flag
        :param group = 0: Group Number
        :return: a Write16 instance
        """
        return Write16(self, lba, tl, data, **kwargs)

