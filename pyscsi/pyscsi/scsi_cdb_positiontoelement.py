# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI PositionToElement command and definitions
#


class PositionToElement(SCSICommand):
    """
    A class to hold information from a PositionToElement command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'medium_transport_address': [0xffff, 2],
                 'destination_address': [0xffff, 4],
                 'invert': [0x01, 8], }

    def __init__(self,
                 opcode,
                 xfer,
                 dest,
                 invert=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param xfer: medium transport address
        :param dest: destination address
        :param invert: invert can be 0 or 1
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             0)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  medium_transport_address=xfer,
                                  destination_address=dest,
                                  invert=invert)
