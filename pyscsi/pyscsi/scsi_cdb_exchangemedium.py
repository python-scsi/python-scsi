# coding: utf-8

# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI ExchangeMedium command and definitions
#


class ExchangeMedium(SCSICommand):
    """
    A class to hold information from a ExchangeMedium command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'medium_transport_address': [0xffff, 2],
                 'source_address': [0xffff, 4],
                 'first_destination_address': [0xffff, 6],
                 'second_destination_address': [0xffff, 8],
                 'inv2': [0x01, 10],
                 'inv1': [0x02, 10], }

    def __init__(self,
                 opcode,
                 xfer,
                 source,
                 dest1,
                 dest2,
                 inv1=0,
                 inv2=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param xfer: medium transfer address
        :param source: source address
        :param dest1: first destination address
        :param dest2: second destination address
        :param inv1: value indicating if first destination should be inverted
        :param inv2: value indicating if scond destination should be inverted
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             0)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  medium_transport_address=xfer,
                                  source_address=source,
                                  first_destination_address=dest1,
                                  second_destination_address=dest2,
                                  inv1=inv1,
                                  inv2=inv2)
