# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI Write12 command and definitions
#


class Write12(SCSICommand):
    """
    A class to send a Write(12) command to a scsi device
    """

    _cdb_bits = {
        "opcode": [0xFF, 0],
        "wrprotect": [0xE0, 1],
        "dpo": [0x10, 1],
        "fua": [0x08, 1],
        "lba": [0xFFFFFFFF, 2],
        "group": [0x1F, 10],
        "tl": [0xFFFFFFFF, 6],
    }

    def __init__(
        self, opcode, blocksize, lba, tl, data, wrprotect=0, dpo=0, fua=0, group=0
    ):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param blocksize: a blocksize
        :param lba: Logical Block Address
        :param tl: transfer length
        :param data: a byte array with data
        :param wrprotect=0:
        :param dpo=0:
        :param fua=0:
        :param group=0:
        """
        if blocksize == 0:
            raise SCSICommand.MissingBlocksizeException

        SCSICommand.__init__(self, opcode, blocksize * tl, 0)
        self.dataout = data
        self.cdb = self.build_cdb(
            opcode=self.opcode.value,
            lba=lba,
            tl=tl,
            wrprotect=wrprotect,
            dpo=dpo,
            fua=fua,
            group=group,
        )
