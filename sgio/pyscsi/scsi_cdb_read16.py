# coding: utf-8

from scsi_command import SCSICommand, OPCODE
from sgio.utils.converter import scsi_int_to_ba, scsi_ba_to_int

#
# SCSI Read16 command and definitions
#

class Read16(SCSICommand):
    """
    A class to send a Read(16) command to a scsi device
    """

    def __init__(self, scsi, lba, tl, **kwargs):
        SCSICommand.__init__(self, scsi, 0, scsi.blocksize * tl)
        self.cdb = self.build_cdb(lba, tl, **kwargs)
        self.execute()

    def build_cdb(self, lba, tl, rdprotect=0, dpo=0, fua=0, rarc=0, group=0):
        """
        Build a Read16 CDB
        """
        cdb = SCSICommand.init_cdb(OPCODE.READ_16)
        cdb[2:10] = scsi_int_to_ba(lba, 8)
        cdb[10:14] = scsi_int_to_ba(tl, 4)
        cdb[1] |= (rdprotect << 5) & 0xe0
        cdb[1] |= 0x10 if dpo else 0
        cdb[1] |= 0x08 if fua else 0
        cdb[1] |= 0x04 if rarc else 0
        cdb[14] |= group & 0x1f

        return cdb
