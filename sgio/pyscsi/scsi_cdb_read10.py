# coding: utf-8

from scsi_command import SCSICommand, OPCODE
from sgio.utils.converter import scsi_int_to_ba, scsi_ba_to_int

#
# SCSI Read10 command and definitions
#

class Read10(SCSICommand):
    """
    A class to send a Read(10) command to a scsi device
    """

    def __init__(self, scsi, lba, tl, **kwargs):
        SCSICommand.__init__(self, scsi, 0, scsi.blocksize * tl)
        self.cdb = self.build_cdb(lba, tl, **kwargs)
        self.execute()

    def build_cdb(self, lba, tl, rdprotect=0, dpo=0, fua=0, rarc=0, group=0):
        """
        Build a Read10 CDB
        """
        cdb = SCSICommand.init_cdb(OPCODE.READ_10)
        cdb[2:6] = scsi_int_to_ba(lba, 4)
        cdb[7:9] = scsi_int_to_ba(tl, 2)
        cdb[1] |= (rdprotect << 5) & 0xe0
        cdb[1] |= 0x10 if dpo else 0
        cdb[1] |= 0x08 if fua else 0
        cdb[1] |= 0x04 if rarc else 0
        cdb[6] |= group & 0x1f

        return cdb
