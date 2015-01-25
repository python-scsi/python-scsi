# coding: utf-8

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE
from pyscsi.utils.converter import scsi_int_to_ba, encode_dict ,decode_bits

#
# SCSI WriteSame16 command and definitions
#


class WriteSame16(SCSICommand):
    """
    A class to send a WriteSame(16) command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'wrprotect': [0xe0, 1],
                 'anchor': [0x10, 1],
                 'unmap': [0x08, 1],
                 'ndob': [0x01, 1],
                 'lba': [0xffffffffffffffff, 2],
                 'group': [0x1f, 14],
                 'nb': [0xffffffff, 10]
    }

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
        cdb = {
            'opcode': self.scsi.device.opcodes.WRITE_SAME_16.value,
            'lba': lba,
            'nb': nb,
            'wrprotect': wrprotect,
            'anchor': anchor,
            'unmap': unmap,
            'ndob': ndob,
            'group': group,
        }
        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a WriteSame16 cdb
        """
        result = {}
        decode_bits(cdb, WriteSame16._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a WriteSame16 cdb
        """
        result = bytearray(16)
        encode_dict(cdb, WriteSame16._cdb_bits, result)
        return result
