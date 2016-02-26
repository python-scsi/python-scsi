# coding: utf-8

from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.utils.converter import encode_dict, decode_bits

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
                 'nb': [0xffffffff, 10], }

    def __init__(self, opcode, blocksize, lba, nb, data, wrprotect=0, anchor=0, unmap=0, ndob=0, group=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param blocksize: a blocksize
        :param lba: logical block address
        :param nb: number of logical blocks
        :param data: a byte array with data
        :param wrprotect: value to specify write protection information
        :param anchor: anchor can have a value of 0 or 1
        :param unmap: unmap can have a value of 0 or 1
        :param ndob: Value can be 0 or 1, use logical block data from data out buffer (data arg) if set to 1.
        :param group: group number, can be 0 or greater
        """
        if not ndob and blocksize == 0:
            raise SCSICommand.MissingBlocksizeException

        SCSICommand.__init__(self, opcode, 0 if ndob else blocksize, 0)
        self.dataout = None if ndob else data
        self.cdb = self.build_cdb(lba, nb, wrprotect, anchor, unmap, ndob, group)

    def build_cdb(self, lba, nb, wrprotect, anchor, unmap, ndob, group):
        """
        Build a WriteSame16 CDB

        :param lba: logical block address
        :param nb: number of logical blocks
        :param wrprotect: value to specify write protection information
        :param anchor: anchor can have a value of 0 or 1
        :param unmap: unmap can have a value of 0 or 1
        :param ndob: Value can be 0 or 1, use logical block data from data out buffer (data arg) if set to 1.
        :param group: group number, can be 0 or greater
        """
        cdb = {
            'opcode': self.opcode.value,
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

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb, WriteSame16._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a WriteSame16 cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(16)
        encode_dict(cdb, WriteSame16._cdb_bits, result)
        return result
