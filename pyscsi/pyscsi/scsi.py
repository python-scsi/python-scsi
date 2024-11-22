# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_cdb_atapassthrough12 import ATAPassThrough12
from pyscsi.pyscsi.scsi_cdb_atapassthrough16 import ATAPassThrough16
from pyscsi.pyscsi.scsi_cdb_exchangemedium import ExchangeMedium
from pyscsi.pyscsi.scsi_cdb_extended_copy_spc4 import ExtendedCopy as ExtendedCopy4
from pyscsi.pyscsi.scsi_cdb_extended_copy_spc5 import ExtendedCopy as ExtendedCopy5
from pyscsi.pyscsi.scsi_cdb_getlbastatus import GetLBAStatus
from pyscsi.pyscsi.scsi_cdb_initelementstatus import InitializeElementStatus
from pyscsi.pyscsi.scsi_cdb_initelementstatuswithrange import (
    InitializeElementStatusWithRange,
)
from pyscsi.pyscsi.scsi_cdb_inquiry import Inquiry
from pyscsi.pyscsi.scsi_cdb_modesense6 import ModeSelect6, ModeSense6
from pyscsi.pyscsi.scsi_cdb_modesense10 import ModeSelect10, ModeSense10
from pyscsi.pyscsi.scsi_cdb_movemedium import MoveMedium
from pyscsi.pyscsi.scsi_cdb_openclose_exportimport_element import (
    OpenCloseImportExportElement,
)
from pyscsi.pyscsi.scsi_cdb_persistentreservein import *
from pyscsi.pyscsi.scsi_cdb_persistentreserveout import PersistentReserveOut
from pyscsi.pyscsi.scsi_cdb_positiontoelement import PositionToElement
from pyscsi.pyscsi.scsi_cdb_preventallow_mediumremoval import PreventAllowMediumRemoval
from pyscsi.pyscsi.scsi_cdb_read10 import Read10
from pyscsi.pyscsi.scsi_cdb_read12 import Read12
from pyscsi.pyscsi.scsi_cdb_read16 import Read16
from pyscsi.pyscsi.scsi_cdb_readcapacity10 import ReadCapacity10
from pyscsi.pyscsi.scsi_cdb_readcapacity16 import ReadCapacity16
from pyscsi.pyscsi.scsi_cdb_readcd import ReadCd
from pyscsi.pyscsi.scsi_cdb_readdiscinformation import ReadDiscInformation
from pyscsi.pyscsi.scsi_cdb_readelementstatus import ReadElementStatus
from pyscsi.pyscsi.scsi_cdb_report_luns import ReportLuns
from pyscsi.pyscsi.scsi_cdb_report_priority import ReportPriority
from pyscsi.pyscsi.scsi_cdb_report_target_port_groups import ReportTargetPortGroups
from pyscsi.pyscsi.scsi_cdb_synchronize_cache10 import SynchronizeCache10
from pyscsi.pyscsi.scsi_cdb_synchronize_cache16 import SynchronizeCache16
from pyscsi.pyscsi.scsi_cdb_testunitready import TestUnitReady
from pyscsi.pyscsi.scsi_cdb_write10 import Write10
from pyscsi.pyscsi.scsi_cdb_write12 import Write12
from pyscsi.pyscsi.scsi_cdb_write16 import Write16
from pyscsi.pyscsi.scsi_cdb_writesame10 import WriteSame10
from pyscsi.pyscsi.scsi_cdb_writesame16 import WriteSame16
from pyscsi.pyscsi.scsi_enum_command import mmc, sbc, smc, spc, ssc
from pyscsi.utils.converter import get_opcode


class SCSI(object):
    """
    The interface to  the specialized scsi classes
    """

    def __init__(self, dev, blocksize=0):
        """
        initialize a new instance

        :param dev: a SCSIDevice object
        :param blocksize:  integer defining a blocksize
        """
        self.device = dev
        self._blocksize = blocksize
        self.__init_opcode()

    def __call__(self, dev):
        """
        call the instance again with new device

        :param dev: a SCSIDevice or ISCSIDevice object
        """
        self.device = dev
        self.__init_opcode()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.device.close()

    def __init_opcode(self):
        """
        Small helper method to terminate the type of
        the scsi device and assigning a proper opcode
        mapper.
        """
        if self.device is not None:
            self.device.devicetype = self.inquiry().result["peripheral_device_type"]
            if self.device.devicetype in (
                0x00,
                0x04,
                0x07,
            ):  # sbc
                self.device.opcodes = sbc
            elif self.device.devicetype in (0x01, 0x02, 0x09):  # ssc
                self.device.opcodes = ssc
            elif self.device.devicetype in (0x03,):  # spc
                self.device.opcodes = spc
            elif self.device.devicetype in (0x08,):  # smc
                self.device.opcodes = smc
            elif self.device.devicetype in (0x05,):  # mmc
                self.device.opcodes = mmc

    def execute(self, cmd, en_raw_sense=False):
        """
        wrapper method to call the SCSIDevice.execute method

        :param cmd: a SCSICommand object
        """
        try:
            self.device.execute(cmd, en_raw_sense=en_raw_sense)
        except Exception as e:
            raise e

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
        Returns a ExchangeMedium Instance

        :param xfer: medium transport element to use
        :param source: source element
        :param dest1: destination 1 element
        :param dest2: destination 2 element
        :param kwargs: inv1=0 invert/rotate the medium before loading
                       inv2=0 invert/rotate the medium before loading
        :return: an ExchangeMedium instance
        """
        opcode = self.device.opcodes.EXCHANGE_MEDIUM
        cmd = ExchangeMedium(opcode, xfer, source, dest1, dest2, **kwargs)
        self.execute(cmd)
        return cmd

    def getlbastatus(self, lba, **kwargs):
        """
        Returns a GetLBAStatus Instance

        :param lba: starting lba
        :param kwargs: a dict with key/value pairs
                       alloc_len = 16384: size of requested datain
        :return: a GetLBAStatus instance
        """
        opcode = next(get_opcode(self.device.opcodes, "9E"))
        cmd = GetLBAStatus(opcode, lba, **kwargs)
        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def inquiry(self, evpd=0, page_code=0, alloclen=96):
        """
        Returns a Inquiry Instance

        :param evpd: a byte indicating if vital product data is supported
        :param page_code: a byte representing a page code for vpd
        :param alloclen: the size of the data_in buffer
        :return: a Inquiry instance
        """
        opcode = self.device.opcodes.INQUIRY
        cmd = Inquiry(opcode, evpd=evpd, page_code=page_code, alloclen=alloclen)
        self.execute(cmd)
        cmd.unmarshall(evpd=evpd)
        return cmd

    def initializeelementstatus(self):
        """
        Returns a InitializeElementStatus Instance

        :return: a InitializeElementStatus instance
        """
        opcode = self.device.opcodes.INITIALIZE_ELEMENT_STATUS
        cmd = InitializeElementStatus(opcode)
        self.execute(cmd)
        return cmd

    def initializeelementstatuswithrange(self, xfer, elements, **kwargs):
        """
        Returns a InitializeElementStatusWithRange Instance

        :param xfer: two byte indicating the address of the starting element
        :param elements: two byte representing a range of elements that should be
                         initialized
        :param kwargs: a dict with key/value pairs
                       range = 0, a integer indicating if elements should be ignored
                       fast = 0, a integer indicating if  elements should be scanned for
                                 media presence
        :return: a InitializeElementStatusWithRange instance
        """
        opcode = self.device.opcodes.INITIALIZE_ELEMENT_STATUS_WITH_RANGE
        cmd = InitializeElementStatusWithRange(opcode, xfer, elements, **kwargs)
        self.execute(cmd)
        return cmd

    def modeselect6(self, data, **kwargs):
        """
        Returns a ModeSelect6 Instance

        :param data: a dict containing the mode page to set
        :param kwargs: a dict with key/value pairs
                       pf = 0, Page Format flag
                       sp = 0, Save Pages flag
        :return: a ModeSelect6 instance
        """
        opcode = self.device.opcodes.MODE_SELECT_6
        cmd = ModeSelect6(opcode, data, **kwargs)
        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def modesense6(self, page_code, **kwargs):
        """
        Returns a ModeSense6 Instance

        :param page_code:  The page requested
        :param kwargs: a dict with key/value pairs
                       sub_page_code = 0, Requested subpage
                       dbd = 0, Disable Block Descriptors flag
                       pc = 0, Page Control flag
                       alloclen = 96
        :return: a ModeSense6 instance
        """
        opcode = self.device.opcodes.MODE_SENSE_6
        cmd = ModeSense6(opcode, page_code, **kwargs)
        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def modesense10(self, page_code, **kwargs):
        """
        Returns a ModeSense10 Instance

        :param page_code:  The page requested
        :param kwargs: a dict with key/value pairs
                       llbaa = 0, long LBA accepted can be 0 or 1
                       dbd = 0, disable block descriptor can be 0 or 1.
                       pc = 0, page control field, a value between 0 and 3
                       alloclen = 0, the max number of bytes allocated for
                       the data_in buffer
        :return: a ModeSense10 instance
        """
        opcode = self.device.opcodes.MODE_SENSE_10
        cmd = ModeSense10(opcode, page_code, **kwargs)
        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def modeselect10(self, data, **kwargs):
        """
        Returns a ModeSelect10 Instance

        :param data: a dict containing the mode page to set
        :param kwargs: a dict with key/value pairs
                       pf = 0, Page Format flag
                       sp = 0, Save Pages flag
        :return: a ModeSelect10 instance
        """
        opcode = self.device.opcodes.MODE_SELECT_10
        cmd = ModeSelect10(opcode, data, **kwargs)
        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def opencloseimportexportelement(self, xfer, acode, **kwargs):
        """
        Returns a OpenCloseImportExportElement Instance

        :param xfer: a dict containing the mode page to set
        :param acode: Page Format flag
        :param kwargs: a dict with key/value pairs
        :return: a OpenCloseImportExportElement instance
        """
        opcode = self.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT
        cmd = OpenCloseImportExportElement(opcode, xfer, acode, **kwargs)
        self.execute(cmd)
        return cmd

    def positiontoelement(self, xfer, dest, **kwargs):
        """
        Returns a PositionToElement Instance

        :param xfer: medium transport element to use
        :param dest: destination element
        :param kwargs: a dict with key/value pairs
                       invert=0, invert/rotate the medium before loading
        :return: an PositionToElement instance
        """
        opcode = self.device.opcodes.POSITION_TO_ELEMENT
        cmd = PositionToElement(opcode, xfer, dest, **kwargs)
        self.execute(cmd)
        return cmd

    def preventallowmediumremoval(self, **kwargs):
        """
        Returns a PreventAllowMediumRemoval Instance

        :param kwargs: a dict with key/value pairs
                       prevent=0, prevent/allow the medium to be removed
        :return: an PreventAllowMediumRemoval instance
        """
        opcode = self.device.opcodes.PREVENT_ALLOW_MEDIUM_REMOVAL
        cmd = PreventAllowMediumRemoval(opcode=opcode, **kwargs)
        self.execute(cmd)
        return cmd

    def read10(self, lba, tl, **kwargs):
        """
        Returns a Read10 Instance

        :param lba: Logical Block Address
        :param tl: Transfer Length
        :param kwargs: a dict with key/value pairs
                       rdprotect = 0, ReadProtect flags
                       dpo = 0, DisablePageOut flag
                       fua = 0, Force Unit Access flag
                       rarc = 0, Rebuild Assist Recovery control flag
                       group = 0, Group Number
        :returns a Read10 Instance
        """
        opcode = self.device.opcodes.READ_10
        cmd = Read10(opcode, self.blocksize, lba, tl, **kwargs)
        self.execute(cmd)
        return cmd

    def read12(self, lba, tl, **kwargs):
        """
        Returns a Read12 Instance

        :param lba: Logical Block Address
        :param tl: Transfer Length
        :param kwargs: a dict with key/value pairs
                       rdprotect = 0, ReadProtect flags
                       dpo = 0, DisablePageOut flag
                       fua = 0, Force Unit Access flag
                       rarc = 0, Rebuild Assist Recovery control flag
                       group = 0, Group Number
        :returns a Read12 Instance
        """
        opcode = self.device.opcodes.READ_12
        cmd = Read12(opcode, self.blocksize, lba, tl, **kwargs)
        self.execute(cmd)
        return cmd

    def read16(self, lba, tl, **kwargs):
        """
        Returns a Read16 Instance

        :param lba: Logical Block Address
        :param tl: Transfer Length
        :param kwargs: a dict with key/value pairs
                       rdprotect = 0, ReadProtect flags
                       dpo = 0, DisablePageOut flag
                       fua = 0, Force Unit Access flag
                       rarc = 0, Rebuild Assist Recovery control flag
                       group = 0, Group Number
        :returns a Read16 Instance
        """
        opcode = self.device.opcodes.READ_16
        cmd = Read16(opcode, self.blocksize, lba, tl, **kwargs)
        self.execute(cmd)
        return cmd

    def readcapacity10(self, **kwargs):
        """
        Returns a ReadCapacity10 Instance

        :param kwargs: a dict with key/value pairs
                       alloc_len = 8, size of requested datain
        :return: a ReadCapacity10 instance
        """
        opcode = self.device.opcodes.READ_CAPACITY_10
        cmd = ReadCapacity10(opcode=opcode, **kwargs)
        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def readcapacity16(self, **kwargs):
        """
        Returns a ReadCapacity16 Instance

        :param kwargs: a dict with key/value pairs
                       alloc_len = 32, size of requested datain
        :return: a ReadCapacity16 instance
        """
        opcode = next(get_opcode(self.device.opcodes, "9E"))
        cmd = ReadCapacity16(opcode=opcode, **kwargs)
        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def readcd(self, lba, tl, **kwargs):
        """
        Returns a ReadCd Instance

        :param lba: Logical Block Address
        :param tl: Transfer Length
        :param kwargs: a dict with key/value pairs
                       est=0: Expected Sector Type
                       dap=0: Digital Audio Play
                       mcsb=0: Main Channel Selection Bits
                       c2e1=0: C2 Error Information
                       scsb=0: Sub-Channel Selection Bits
        :return: a ReadCd instance
        """
        opcode = self.device.opcodes.READ_CD
        cmd = ReadCd(opcode, lba, tl, **kwargs)
        self.execute(cmd)
        cmd.unmarshall(lba=lba, tl=tl, **kwargs)
        return cmd

    def readdiscinformation(self, data_type, alloc_len=4096):
        """
        Returns a ReadDiscInformation Instance

        :param data_type: Data Type
        :param alloc_len: Allocation Length

        :return: a ReadDiscInformation instance
        """
        opcode = self.device.opcodes.READ_DISC_INFORMATION
        cmd = ReadDiscInformation(opcode, data_type, alloc_len=alloc_len)
        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def readelementstatus(self, start, num, **kwargs):
        """
        Returns a ReadElementStatus Instance

        :param start: starting address for first element to return
        :param num: numbver of elements to return
        :param kwargs: a dict with key/value pairs
                       element_type, type of elements to return
                       voltag = 0, whether volume tag data should be returned
                       curdata = 1, check current data
                       dvcid = 0, whether to return device identifiers
                       alloclen=16384, max amount od data to return
        :return: an ReadElementStatus instance
        """
        opcode = self.device.opcodes.READ_ELEMENT_STATUS
        cmd = ReadElementStatus(opcode, start, num, **kwargs)
        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def movemedium(self, xfer, source, dest, **kwargs):
        """
        Returns a MoveMedium Instance

        :param xfer: medium transport element to use
        :param source: source element
        :param dest: destination element
        :param kwargs: a dict with key/value pairs
                       invert=0, invert/rotate the medium before loading
        :return: an MoveMedium instance
        """
        opcode = self.device.opcodes.MOVE_MEDIUM
        cmd = MoveMedium(opcode, xfer, source, dest, **kwargs)
        self.execute(cmd)
        return cmd

    def synchronizecache10(self, lba, numblks, **kwargs):
        """
        Returns a SynchronizeCache10 Instance

        :param lba: Logical Block Address to write to
        :param numblks: number of logical blocks that shall be
                        synchronized, starting with the logical
                        block referenced by the lba
        :param kwargs: a dict with key/value pairs
                       immed = 0, do not return status until the
                                  synchronize cache operation has
                                  been completed.
                       group = 0, Group Number
        :return: a SynchronizeCache10 instance
        """
        opcode = self.device.opcodes.SYNCHRONIZE_CACHE_10
        cmd = SynchronizeCache10(opcode, lba, numblks, **kwargs)
        self.execute(cmd)
        return cmd

    def synchronizecache16(self, lba, numblks, **kwargs):
        """
        Returns a SynchronizeCache16 Instance

        :param lba: Logical Block Address to write to
        :param numblks: number of logical blocks that shall be
                        synchronized, starting with the logical
                        block referenced by the lba
        :param kwargs: a dict with key/value pairs
                       immed = 0, do not return status until the
                                  synchronize cache operation has
                                  been completed.
                       group = 0, Group Number
        :return: a SynchronizeCache16 instance
        """
        opcode = self.device.opcodes.SYNCHRONIZE_CACHE_16
        cmd = SynchronizeCache16(opcode, lba, numblks, **kwargs)
        self.execute(cmd)
        return cmd

    def testunitready(self):
        """
        Returns a TestUnitReady Instance

        """
        opcode = self.device.opcodes.TEST_UNIT_READY
        cmd = TestUnitReady(opcode)
        self.execute(cmd)
        return cmd

    def write10(self, lba, tl, data, **kwargs):
        """
        Returns a Write10 Instance

        :param lba: Logical Block Address to write to
        :param tl: Transfer Length in blocks
        :param data: bytearray containing the data to write
        :param kwargs: a dict with key/value pairs
                       wrprotect = 0, WriteProtect flags
                       dpo = 0, disable Page Out flag
                       fua = 0, Force Unit Access flag
                       group = 0, Group Number
        :return: a Write10 instance
        """
        opcode = self.device.opcodes.WRITE_10
        cmd = Write10(opcode, self.blocksize, lba, tl, data, **kwargs)
        self.execute(cmd)
        return cmd

    def write12(self, lba, tl, data, **kwargs):
        """
        Returns a Write12 Instance

        :param lba: Logical Block Address to write to
        :param tl: Transfer Length in blocks
        :param data: bytearray containing the data to write
        :param kwargs: a dict with key/value pairs
                       wrprotect = 0, WriteProtect flags
                       dpo = 0, disable Page Out flag
                       fua = 0, Force Unit Access flag
                       group = 0, Group Number
        :return: a Write12 instance
        """
        opcode = self.device.opcodes.WRITE_12
        cmd = Write12(opcode, self.blocksize, lba, tl, data, **kwargs)
        self.execute(cmd)
        return cmd

    def write16(self, lba, tl, data, **kwargs):
        """
        Returns a Write16 Instance

        :param lba: Logical Block Address to write to
        :param tl: Transfer Length in blocks
        :param data: bytearray containing the data to write
        :param kwargs: a dict with key/value pairs
                       wrprotect = 0, WriteProtect flags
                       dpo = 0, disable Page Out flag
                       fua = 0, Force Unit Access flag
                       group = 0, Group Number
        :return: a Write16 instance
        """
        opcode = self.device.opcodes.WRITE_16
        cmd = Write16(opcode, self.blocksize, lba, tl, data, **kwargs)
        self.execute(cmd)
        return cmd

    def writesame16(self, lba, nb, data, **kwargs):
        """
        Returns a WriteSame16 Instance

        :param lba: Logical Block Address to write to
        :param nb: Number of blocks
        :param data: bytearray containing the block to write
        :param kwargs: a dict with key/value pairs
                       wrprotect = 0, WriteProtect flags
                       anchor = 0, Anchor flag
                       unmap = 0, Unmap flag
                       ndob = 0, NoDataOutBuffer flag. When set data is None.
                       group = 0, Group Number
        :return: a WriteSame16 instance
        """
        opcode = self.device.opcodes.WRITE_SAME_16
        cmd = WriteSame16(opcode, self.blocksize, lba, nb, data, **kwargs)
        self.execute(cmd)
        return cmd

    def writesame10(self, lba, nb, data, **kwargs):
        """
        Returns a WriteSame10 Instance

        :param lba: Logical Block Address to write to
        :param nb: Number of blocks
        :param data: bytearray containing the block to write
        :param kwargs: a dict with key/value pairs
                       wrprotect = 0, WriteProtect flags
                       anchor = 0, Anchor flag
                       unmap = 0, Unmap flag
                       group = 0, Group Number
        :return: a WriteSame10 instance
        """
        opcode = self.device.opcodes.WRITE_SAME_10
        cmd = WriteSame10(opcode, self.blocksize, lba, nb, data, **kwargs)
        self.execute(cmd)
        return cmd

    def reportluns(self, **kwargs):
        """
        Return a ReportLuns Instance

        :param kwargs: a dict with key/value pairs
                       report=0x00, type of logical unit addresses that shall be reported
                       alloclen=96, size of requested datain
        :return: a ReportLuns instance
        """
        opcode = self.device.opcodes.REPORT_LUNS
        cmd = ReportLuns(opcode=opcode, **kwargs)
        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def reportpriority(self, **kwargs):
        """
        Return a ReportPriority Instance

        :param kwargs: a dict with key/value pairs
                       priority=0, specifies information to be returned in data_in buffer
                       alloclen=16384, size of requested datain
        :return: a ReportLuns instance
        """
        opcode = next(get_opcode(self.device.opcodes, "A3"))
        cmd = ReportPriority(opcode=opcode, **kwargs)
        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def reporttargetportgroups(self, **kwargs):
        """
        Return a ReportTargetPortGroups Instance

        :param kwargs: a dict with key/value pairs
                       data_format=0x00, specifies the requested format for the parameter
                       data returned
                       alloclen=16384, size of requested datain
        :return: a ReportTargetPortGroups instance
        """
        opcode = next(get_opcode(self.device.opcodes, "A3"))
        cmd = ReportTargetPortGroups(opcode=opcode, **kwargs)
        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def atapassthrough12(
        self,
        protocal,
        t_length,
        byte_block,
        t_dir,
        t_type,
        off_line,
        fetures,
        count,
        lba,
        command,
        **kwargs
    ):
        """
        Return a ATAPassThrough12 Instance, check ATA Status Return Descriptor by yourself

        :param protocal: ATAPassthrough12 PROTOCOL field
        :param t_length: ATAPassthrough12 t_length field
        :param byte_block: ATAPassthrough12 byte_block field
        :param t_dir: ATAPassthrough12 t_dir field
        :param t_type: ATAPassthrough12 t_type field
        :param off_line: ATAPassThrough12 off_line field
        :param fetures: ATAPassThrough12 fetures field
        :param count: ATAPassThrough12 count field
        :param lba: ATAPassThrough12 lba field
        :param command: ATAPassThrough12 command field
        :param kwargs: a dict with key/value pairs
                       blocksize=None: a blocksize
                       extra_tl=None, if t_length=3, can fix the transfer length in this option
                       ck_cond=0: ATAPassThrough12 ck_cond field
                       device=0: ATAPassThrough12 device field
                       control=0: ATAPassThrough12 control field
                       data=None: a byte array with data, if command need data-in data-out
        :return: a ATAPassThrough12 instance
        """
        opcode = self.device.opcodes.ATA_PASS_THROUGH_12
        cmd = ATAPassThrough12(
            opcode,
            protocal,
            t_length,
            byte_block,
            t_dir,
            t_type,
            off_line,
            fetures,
            count,
            lba,
            command,
            **kwargs
        )
        self.execute(cmd, en_raw_sense=True)
        return cmd

    def atapassthrough16(
        self,
        protocal,
        t_length,
        byte_block,
        t_dir,
        t_type,
        off_line,
        fetures,
        count,
        lba,
        command,
        **kwargs
    ):
        """
        Return a ATAPassThrough16 Instance, check ATA Status Return Descriptor by yourself

        :param protocal: ATAPassThrough16 PROTOCOL field
        :param t_length: ATAPassThrough16 t_length field
        :param byte_block: ATAPassThrough16 byte_block field
        :param t_dir: ATAPassThrough16 t_dir field
        :param t_type: ATAPassThrough16 t_type field
        :param off_line: ATAPassThrough16 off_line field
        :param fetures: ATAPassThrough16 fetures field
        :param count: ATAPassThrough16 count field
        :param lba: ATAPassThrough16 lba field
        :param command: ATAPassThrough16 command field
        :param kwargs: a dict with key/value pairs
                       blocksize=None: a blocksize
                       extra_tl=None, if t_length=3, can fix the transfer length in this option
                       ck_cond=0: ATAPassThrough16 ck_cond field
                       device=0: ATAPassThrough16 device field
                       control=0: ATAPassThrough16 control field
                       data=None: a byte array with data, if command need data-in data-out
                       extend=1: ATAPassthrough16 extend field
        :return: a ATAPassThrough16 instance
        """
        opcode = self.device.opcodes.ATA_PASS_THROUGH_16
        cmd = ATAPassThrough16(
            opcode,
            protocal,
            t_length,
            byte_block,
            t_dir,
            t_type,
            off_line,
            fetures,
            count,
            lba,
            command,
            **kwargs
        )
        self.execute(cmd, en_raw_sense=True)
        return cmd

    def persistentreservein(self, service_action, **kwargs):
        """
        Return a PersistentReserveIn Instance

        :param service_action: an int, the SERVICE ACTION code
        :param kwargs: a dict with key/value pairs
                       alloclen=1024, size of requested datain
        :return: a PersistentReserveIn instance
        """
        opcode = self.device.opcodes.PERSISTENT_RESERVE_IN
        if service_action == opcode.serviceaction.READ_KEYS:
            cmd = PersistentReserveInReadKeys(opcode=opcode, **kwargs)
        elif service_action == opcode.serviceaction.READ_RESERVATION:
            cmd = PersistentReserveInReadReservation(opcode=opcode, **kwargs)
        elif service_action == opcode.serviceaction.REPORT_CAPABILITIES:
            cmd = PersistentReserveInReportCapabilities(opcode=opcode, **kwargs)
        elif service_action == opcode.serviceaction.READ_FULL_STATUS:
            cmd = PersistentReserveInReadFullStatus(opcode=opcode, **kwargs)
        else:
            raise ValueError("Invalid Service Action")

        self.execute(cmd)
        cmd.unmarshall()
        return cmd

    def persistentreserveout(self, service_action, scope=0, pr_type=0, **kwargs):
        """
        Returns a PersistentReserveOut Instance

        :param service_action: an int, the SERVICE ACTION code
        :param scope: persistent reservation SCOPE field
        :param pr_type: persistent reservation TYPE field
        :param kwargs: a dict with key/value pairs to specify the parameter
                       list, either a Basic parameter list or a Register and
                       Move parameter list


        Basic parameter list may have the following keys:
            reservation_key: eight-byte value to identify the I_T nexus that
                             is the source of the PERSISTENT RESERVE OUT command
            service_action_reservation_key: eight-byte value containing the
                             reservation key to be registered to the specified
                             I_T nexus
            spec_i_pt: bit, Specify Initiator Ports (SPEC_I_PT)
            all_tg_pt: bit, All Target Ports
            aptpl: bit, Activate Persist Through Power Loss
            transport_ids: a list of TransportID dicts used with REGISTER when
                           spec_i_pt is set.

        Each TransportID dict may have keys:
            protocol_id, an int, specifies the SCSI transport protocol
            tpid_format, an int, specifies the the format of the TransportID
            n_port_name, 8-byte value, applicable to FIBRE_CHANNEL protocol_id
            eui64_name, 8-byte value, applicable to IEEE_1394 protocol_id
            initiator_port_identifier, 16-byte value, applicable to RDMA
                                        protocol_id
            iscsi_name, string representing IQN of initiator, applicable to
                        iSCSI protocol_id
            iscsi_initiator_session_id, string containing the iSCSI initiator
                                        session identifier (see RFC 7143) in
                                        the form of ASCII characters that are
                                        the hexadecimal digits converted from
                                        the binary iSCSI initiator session
                                        identifier value.  Applicable to ISCSI
                                        protocol_id when tpid_format=1
            sas_address, 8-byte value, applicable to SAS protocol_id
            routing_id, 8-byte value, applicable to SOP (SCSI over PCI Express)
                                      protocol_id

        Register and Move parameter list may have the following keys:
            reservation_key: as described in Basic parameter list
            service_action_reservation_key: as described in Basic parameter list
            unreg: bit, Unregister
            aptpl: bit, Activate Persist Through Power Loss
            relative_target_port_id: 2-byte int, the relative port identifier of
                                     the target port in the I_T nexus to which
                                     the persistent reservation is to be moved.
            transport_id: a TransportID dict

        :return: a PersistentReserveOut instance
        """
        opcode = self.device.opcodes.PERSISTENT_RESERVE_OUT
        cmd = PersistentReserveOut(opcode, service_action, scope, pr_type, **kwargs)
        self.execute(cmd)
        return cmd

    def extendedcopy4(
        self,
        list_identifier=0,
        sequential_striped=0,
        nrcr=0,
        priority=0,
        target_descriptor_list=[],
        segment_descriptor_list=[],
        inline_data=bytearray(0),
    ):
        opcode = self.device.opcodes.EXTENDED_COPY
        cmd = ExtendedCopy4(
            opcode,
            list_identifier,
            sequential_striped,
            nrcr,
            priority,
            target_descriptor_list,
            segment_descriptor_list,
            inline_data,
        )
        self.execute(cmd)
        return cmd

    def extendedcopy5(
        self,
        sequential_striped=0,
        list_id_usage=0,
        priority=0,
        g_sense=0,
        immed=0,
        list_identifier=0,
        cscd_descriptor_list=[],
        segment_descriptor_list=[],
        inline_data=bytearray(0),
    ):
        opcode = self.device.opcodes.EXTENDED_COPY
        cmd = ExtendedCopy5(
            opcode,
            sequential_striped,
            list_id_usage,
            priority,
            g_sense,
            immed,
            list_identifier,
            cscd_descriptor_list,
            segment_descriptor_list,
            inline_data,
        )
        self.execute(cmd)
        return cmd
