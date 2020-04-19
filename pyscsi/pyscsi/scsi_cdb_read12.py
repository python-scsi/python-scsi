# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI Read12 command and definitions
#


class Read12(SCSICommand):
    """
    A class to send a Read(12) command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'rdprotect': [0xe0, 1],
                 'dpo': [0x10, 1],
                 'fua': [0x08, 1],
                 'rarc': [0x04, 1],
                 'lba': [0xffffffff, 2],
                 'tl': [0xffffffff, 6],
                 'group': [0x1f, 10], }

    def __init__(self,
                 opcode,
                 blocksize,
                 lba,
                 tl,
                 rdprotect=0,
                 dpo=0,
                 fua=0,
                 rarc=0,
                 group=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param blocksize: a blocksize
        :param lba: Logical Block Address
        :param tl: transfer length
        :param rdprotect=0:
        :param dpo=0:
        :param fua=0:
        :param rarc=0:
        :param group=0:
        """
        if blocksize == 0:
            raise SCSICommand.MissingBlocksizeException

        SCSICommand.__init__(self,
                             opcode,
                             0,
                             blocksize * tl)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  lba=lba,
                                  tl=tl,
                                  rdprotect=rdprotect,
                                  dpo=dpo,
                                  fua=fua,
                                  rarc=rarc,
                                  group=group)
