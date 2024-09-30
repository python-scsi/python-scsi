# coding: utf-8

# Copyright (C) 2024 by Brian Meagher<brian.meagher@ixsystems.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI SYNCHRONIZE CACHE 16 command and definitions
#
# See SBC-4 5.34 SYNCHRONIZE CACHE (16) command
#


class SynchronizeCache16(SCSICommand):
    """
    A class to send a Synchronize Cache (16) command to a scsi device
    """

    _cdb_bits = {
        "opcode": [0xFF, 0],
        "immed": [0x02, 1],
        "lba": [0xFFFFFFFFFFFFFFFF, 2],
        "numblks": [0xFFFFFFFF, 10],
        "group": [0x1F, 14],
    }

    def __init__(self, opcode, lba, numblks, immed=0, group=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param lba: Logical Block Address
        :param numblks: transfer length
        :param immed=0:
        :param group=0:
        """
        SCSICommand.__init__(self, opcode, 0, 0)
        self.cdb = self.build_cdb(
            opcode=self.opcode.value,
            lba=lba,
            numblks=numblks,
            immed=immed,
            group=group,
        )
