# coding: utf-8

# Copyright:
#  Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
#  Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
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

from scsi_cdb_exchangemedium import ExchangeMedium
from scsi_cdb_getlbastatus import GetLBAStatus
from scsi_cdb_inquiry import Inquiry
from scsi_cdb_modesense6 import ModeSense6, ModeSelect6
from scsi_cdb_modesense10 import ModeSense10, ModeSelect10
from scsi_cdb_movemedium import MoveMedium
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
from scsi_cdb_writesame10 import WriteSame10
from scsi_cdb_writesame16 import WriteSame16
from scsi_enum_command import spc, sbc, smc, ssc, mmc


class SCSI(object):
    """
    The interface to  the specialized scsi classes
    """
    def __init__(self, dev):
        self.device = dev
        self._blocksize = 0
        self.__init_opcode()

    def __call__(self, dev):
        self.device = dev
        self.__init_opcode()

    def __init_opcode(self):
        """
        Small helper method to terminate the type of
        the scsi device and assigning a proper opcode
        mapper.
        """
        dev_type = self.inquiry().result['peripheral_device_type']
        if dev_type in (0x00, 0x04, 0x07, ):  # sbc
            self.device.opcodes = sbc
        elif dev_type in (0x01, 0x02, 0x09):  # ssc
            self.device.opcodes = ssc
        elif dev_type in (0x03,):  # spc
            self.device.opcodes = spc
        elif dev_type in (0x08,):  # smc
            self.device.opcodes = smc
        elif dev_type in (0x05,):  # mmc
            self.device.opcodes = mmc

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

    def exchangemedium(self, xfer, source, dest1, dest2, **kwargs):
        """
        Returns a MoveMedium Instance

        :param xfer: medium transport element to use
        :param source: source element
        :param dest: destination element
        :param invert=0: invert/rotate the medium before loading
        :return: an MoveMedium instance
        """
        return ExchangeMedium(self, xfer, source, dest1, dest2, **kwargs)

    def getlbastatus(self, lba, **kwargs):
        """
        Returns a GetLBAStatus Instance

        :param lba: starting lba
        :param alloc_len = 16384: size of requested datain
        :return: a getlbastatus instance
        """
        return GetLBAStatus(self, lba, **kwargs)

    def inquiry(self, **kwargs):
        """
        Returns a Inquiry Instance

        :param evpd = 0: a byte indicating if vital product data is supported
        :param page_code = 0: a byte representing a page code for vpd
        :param alloc_len = 96: a integer , the size of the data_in buffer
        :return: a Inquiry instance
        """
        return Inquiry(self, **kwargs)

    def modeselect6(self, data, **kwargs):
        """
        Returns a ModeSelect6 Instance

        :param data: a dict containing the mode page to set
        :param pf = 0: Page Format flag
        :param sp = 0: Save Pages flag
        :return: a ModeSelect6 instance
        """
        return ModeSelect6(self, data, **kwargs)

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

    def modesense10(self, page_code, **kwargs):
        """
        Returns a ModeSense10 Instance

        :param page_code:  The page requested
        :param sub_page_code = 0: Requested subpage
        :param dbd = 0: Disable Block Descriptors flag
        :param pc = 0: Page Control flag
        :param alloclen = 96
        :return: a ModeSense6 instance
        """
        return ModeSense10(self, page_code, **kwargs)

    def modeselect10(self, data, **kwargs):
        """
        Returns a ModeSelect10 Instance

        :param data: a dict containing the mode page to set
        :param pf = 0: Page Format flag
        :param sp = 0: Save Pages flag
        :return: a ModeSelect6 instance
        """
        return ModeSelect10(self, data, **kwargs)

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

    def movemedium(self, xfer, source, dest, **kwargs):
        """
        Returns a MoveMedium Instance

        :param xfer: medium transport element to use
        :param source: source element
        :param dest: destination element
        :param invert=0: invert/rotate the medium before loading
        :return: an MoveMedium instance
        """
        return MoveMedium(self, xfer, source, dest, **kwargs)

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

    def writesame16(self, lba, nb, data, **kwargs):
        """
        Returns a WriteSame16 Instance

        :param lba: Logical Block Address to write to
        :param nb: Number of blocks
        :param data: bytearray containing the block to write
        :param wrprotect = 0: WriteProtect flags
        :param anchor = False: Anchor flag
        :param unmap = False: Unmap flag
        :param ndob = False: NoDataOutBuffer flag. When set data is None.
        :param group = 0: Group Number
        :return: a WriteSame16 instance
        """
        return WriteSame16(self, lba, nb, data, **kwargs)

    def writesame10(self, lba, nb, data, **kwargs):
        """
        Returns a WriteSame10 Instance

        :param lba: Logical Block Address to write to
        :param nb: Number of blocks
        :param data: bytearray containing the block to write
        :param wrprotect = 0: WriteProtect flags
        :param anchor = False: Anchor flag
        :param unmap = False: Unmap flag
        :param group = 0: Group Number
        :return: a WriteSame10 instance
        """
        return WriteSame10(self, lba, nb, data, **kwargs)
