# coding: utf-8

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE
from pyscsi.utils.converter import scsi_int_to_ba, decode_bits

#
# SCSI WriteSame16 command and definitions
#


class WriteSame16(SCSICommand):
    """
    A class to send a WriteSame(16) command to a scsi device
    """

    def __init__(self, scsi, lba, nb, data, wrprotect=0, anchor=False,
                 unmap=False, ndob=False, group=0):
        self.dataout = None if ndob else data
        SCSICommand.__init__(self, scsi, 0 if ndob else scsi.blocksize, 0)
        self.cdb = self.build_cdb(lba, nb, wrprotect, anchor, unmap,
                                  ndob, group)
        self.execute()

    def build_cdb(self, lba, nb, wrprotect, anchor, unmap,
                  ndob, group):
        """
        Build a WriteSame16 CDB
        """
        cdb = SCSICommand.init_cdb(OPCODE.WRITE_SAME_16)
        cdb[2:10] = scsi_int_to_ba(lba, 8)
        cdb[10:14] = scsi_int_to_ba(nb, 4)
        cdb[1] |= (wrprotect << 5) & 0xe0
        cdb[1] |= 0x10 if anchor else 0
        cdb[1] |= 0x08 if unmap else 0
        cdb[1] |= 0x01 if ndob else 0
        cdb[14] |= group & 0x1f

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
                 'ndob': [0x01, 1],
                 'lba': [0xffffffffffffffff, 2],
                 'group': [0x1f, 14],
                 'nb': [0xffffffff, 10], }
        decode_bits(cdb, _bits, _tmp)
        return _tmp
