# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

# coding: utf-8


from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.utils.converter import decode_bits, encode_dict

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

    def __init__(self,
                 opcode,
                 blocksize,
                 lba,
                 nb,
                 data,
                 wrprotect=0,
                 anchor=0,
                 unmap=0,
                 ndob=0,
                 group=0):
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
        :param ndob: Value can be 0 or 1, use logical block data from data out buffer
                     (data arg) if set to 1.
        :param group: group number, can be 0 or greater
        """
        if not ndob and blocksize == 0:
            raise SCSICommand.MissingBlocksizeException

        SCSICommand.__init__(self,
                             opcode,
                             0 if ndob else blocksize,
                             0)
        self.dataout = None if ndob else data
        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  lba=lba,
                                  nb=nb,
                                  wrprotect=wrprotect,
                                  anchor=anchor,
                                  unmap=unmap,
                                  ndob=ndob,
                                  group=group)
