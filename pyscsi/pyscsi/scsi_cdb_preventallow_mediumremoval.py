# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI PreventAllowMediumRemoval command and definitions
#


class PreventAllowMediumRemoval(SCSICommand):
    """
    A class to hold information from a PositionToElement command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'prevent': [0x03, 4], }

    def __init__(self,
                 opcode,
                 prevent=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param prevent: prevent can have a value between 0 and 3
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             0)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  prevent=prevent)
