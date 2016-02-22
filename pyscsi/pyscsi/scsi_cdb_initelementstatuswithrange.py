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
from pyscsi.utils.converter import encode_dict, decode_bits

#
# SCSI InitializeElementStatusWithRange command and definitions
#


class InitializeElementStatusWithRange(SCSICommand):
    """
    A class to hold information from a InitializeElementStatusWithRange command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0],
                 'fast': [0x02, 1],
                 'range': [0x01, 1],
                 'starting_element_address': [0xffff, 2],
                 'number_of_elements': [0xffff, 6], }

    def __init__(self, scsi, xfer, elements, rng=0, fast=0):
        """
        initialize a new instance

        :param scsi: a SCSI object
        :param xfer: starting element address
        :param elements: number of elements
        :param rng: range  indicates if all elements should be checked, if set to 1 xfer and elements are ignored
        :param fast: fast , if set to 1 scan for media presence only. If set to 0 scan elements for all relevant
                     status.
        """
        SCSICommand.__init__(self, scsi, 0, 0)
        self.cdb = self.build_cdb(xfer, elements, rng, fast)
        self.execute()

    def build_cdb(self, xfer, elements, rng, fast):
        """
        Build a InitializeElementStatusWithRange CDB

        :param xfer: starting element address
        :param elements: number of elements
        :param rng: range can be 0 or 1
        :return: a byte array representing a code descriptor block
        """
        cdb = {'opcode': self.scsi.device.opcodes.INITIALIZE_ELEMENT_STATUS_WITH_RANGE.value,
               'fast': fast,
               'range': rng,
               'starting_element_address': xfer,
               'number_of_elements': elements, }

        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a InitializeElementStatusWithRange cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb, InitializeElementStatusWithRange._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a InitializeElementStatusWithRange cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(10)
        encode_dict(cdb, InitializeElementStatusWithRange._cdb_bits, result)
        return result



