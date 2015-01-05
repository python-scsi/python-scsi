# coding: utf-8

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE
from pyscsi.utils.converter import scsi_int_to_ba, decode_bits

#
# SCSI Write10 command and definitions
#


class Write10(SCSICommand):
    """
    A class to send a Write(10) command to a scsi device
    """

    def __init__(self, scsi, lba, tl, data, **kwargs):
        self.dataout = data
        SCSICommand.__init__(self, scsi, scsi.blocksize * tl, 0)
        self.cdb = self.build_cdb(lba, tl, **kwargs)
        self.execute()

    def build_cdb(self, lba, tl, wrprotect=0, dpo=0, fua=0, group=0):
        """
        Build a Write10 CDB
        """
        cdb = SCSICommand.init_cdb(OPCODE.WRITE_10)
        cdb[2:6] = scsi_int_to_ba(lba, 4)
        cdb[7:9] = scsi_int_to_ba(tl, 2)
        cdb[1] |= (wrprotect << 5) & 0xe0
        cdb[1] |= 0x10 if dpo else 0
        cdb[1] |= 0x08 if fua else 0
        cdb[6] |= group & 0x1f

        return cdb

    def unmarshall_cdb(self, cdb):
        """
        method to unmarshall a byte array containing a cdb.
        """
        _tmp = {}
        _bits = {'opcode': [0xff, 0],
                'wrprotect': [0xe0, 1],
                'dpo': [0x10, 1],
                'fua': [0x08, 1],
                'lba': [0xffffffff, 2],
                'group': [0x1f, 6],
                'tl': [0xffff, 7], }
        decode_bits(cdb, _bits, _tmp)
        return _tmp
