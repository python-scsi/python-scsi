# coding: utf-8

# Copyright:
# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI InitializeElementStatusWithRange command and definitions
#


class InitializeElementStatusWithRange(SCSICommand):
    """
    A class to hold information from a InitializeElementStatusWithRange command
    to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'fast': [0x02, 1],
                 'range': [0x01, 1],
                 'starting_element_address': [0xffff, 2],
                 'number_of_elements': [0xffff, 6], }

    def __init__(self,
                 opcode,
                 xfer,
                 elements,
                 rng=0,
                 fast=0):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param xfer: starting element address
        :param elements: number of elements
        :param rng: range  indicates if all elements should be checked, if set to 1 xfer
                    and elements are ignored
        :param fast: fast , if set to 1 scan for media presence only. If set to 0 scan
                     elements for all relevant status.
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             0)

        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  starting_element_address=xfer,
                                  number_of_elements=elements,
                                  range=rng,
                                  fast=fast)
