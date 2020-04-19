# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI WriteSame10 command and definitions
#


class WriteSame10(SCSICommand):
    """
    A class to send a WriteSame(10) command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'wrprotect': [0xe0, 1],
                 'anchor': [0x10, 1],
                 'unmap': [0x08, 1],
                 'lba': [0xffffffff, 2],
                 'group': [0x1f, 6],
                 'nb': [0xffff, 7], }

    def __init__(self,
                 opcode,
                 blocksize,
                 lba,
                 nb,
                 data,
                 wrprotect=0,
                 anchor=0,
                 unmap=0,
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
        :param group: group number, can be 0 or greater
        """
        if blocksize == 0:
            raise SCSICommand.MissingBlocksizeException

        SCSICommand.__init__(self,
                             opcode,
                             blocksize,
                             0)
        self.dataout = data
        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  lba=lba,
                                  nb=nb,
                                  wrprotect=wrprotect,
                                  anchor=anchor,
                                  unmap=unmap,
                                  group=group)
