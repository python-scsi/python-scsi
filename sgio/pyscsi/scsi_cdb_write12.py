# coding: utf-8

from scsi_command import SCSICommand, OPCODE
from sgio.utils.converter import scsi_int_to_ba, scsi_ba_to_int

#
# SCSI Write12 command and definitions
#

class Write12(SCSICommand):
    """
    A class to send a Write(12) command to a scsi device
    """

    def __init__(self, scsi, lba, tl, data, **kwargs):
        self.dataout = data
        SCSICommand.__init__(self, scsi, scsi.blocksize * tl, 0)
        self.cdb = self.build_cdb(lba, tl, **kwargs)
        self.execute()

    def build_cdb(self, lba, tl, wrprotect=0, dpo=0, fua=0, group=0):
        """
        Build a Read12 CDB
        """
        cdb = SCSICommand.init_cdb(OPCODE.WRITE_12)
        cdb[2:6] = scsi_int_to_ba(lba, 4)
        cdb[6:10] = scsi_int_to_ba(tl, 4)
        cdb[1] |= (wrprotect << 5) & 0xe0
        cdb[1] |= 0x10 if dpo else 0
        cdb[1] |= 0x08 if fua else 0
        cdb[10] |= group & 0x1f

        return cdb
