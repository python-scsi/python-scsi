# coding: utf-8

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE
from pyscsi.utils.converter import scsi_int_to_ba, decode_bits

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

    def unmarshall_cdb(self, cdb):
        """
        method to unmarshall a byte array containing a cdb.
        """
        _tmp = {}
        _bits = {'opcode': [0xff, 0],
                'rdprotect': [0xe0, 1],
                'dpo': [0x10, 1],
                'fua': [0x08, 1],
                'rarc': [0x04, 1],
                'lba': [0xffffffffffffffff, 2],
                'group': [0x1f, 14],
                'tl': [0xffffffff, 10], }
        decode_bits(cdb, _bits, _tmp)
        return _tmp

