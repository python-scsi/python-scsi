# coding: utf-8

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE
from pyscsi.utils.converter import scsi_int_to_ba, decode_bits

#
# SCSI WriteSame10 command and definitions
#


class WriteSame10(SCSICommand):
    """
    A class to send a WriteSame(10) command to a scsi device
    """

    def __init__(self, scsi, lba, nb, data, wrprotect=0, anchor=False,
                 unmap=False, group=0):
        self.dataout = data
        SCSICommand.__init__(self, scsi, scsi.blocksize, 0)
        self.cdb = self.build_cdb(lba, nb, wrprotect, anchor, unmap, group)
        self.execute()

    def build_cdb(self, lba, nb, wrprotect, anchor, unmap, group):
        """
        Build a WriteSame10 CDB
        """
        cdb = SCSICommand.init_cdb(OPCODE.WRITE_SAME_10)
        cdb[2:6] = scsi_int_to_ba(lba, 4)
        cdb[7:9] = scsi_int_to_ba(nb, 2)
        cdb[1] |= (wrprotect << 5) & 0xe0
        cdb[1] |= 0x10 if anchor else 0
        cdb[1] |= 0x08 if unmap else 0
        cdb[6] |= group & 0x1f

        return cdb

    def unmarshall_cdb(self, cdb):
        """
        method to unmarshall a byte array containing a cdb.
        """
        _tmp = {}
        _bits = {'opcode': [0xff, 0],
                'wrprotect': [0xe0, 1],
                'anchor': [0x10, 1],
                'unmap': [0x08, 1],
                'lba': [0xffffffff, 2],
                 'group': [0x1f, 6],
                 'nb': [0xffff, 7], }
        decode_bits(cdb, _bits, _tmp)
        return _tmp
