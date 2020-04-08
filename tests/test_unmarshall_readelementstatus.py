#!/usr/bin/env python
# coding: utf-8
# Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
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

import unittest

from mock_device import MockDevice, MockSCSI
from pyscsi.utils.converter import scsi_int_to_ba
from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.pyscsi import scsi_enum_readelementstatus as READELEMENTSTATUS
from pyscsi.pyscsi.scsi_cdb_readelementstatus import ReadElementStatus


class MockReadElementStatus(MockDevice):

    def execute(self, cmd):
        # element status header data
        data = bytearray(8)
        data[0:2] = scsi_int_to_ba(12, 2)  # first element address reported
        data[2:4] = scsi_int_to_ba(3, 2)   # number of elements available

        # first element status page, containing one element
        _d = bytearray(8)
        _d[0] = READELEMENTSTATUS.ELEMENT_TYPE.STORAGE
        _d[1] = 0x00

        _dd = bytearray(12 + 4)
        _dd[0:2] = scsi_int_to_ba(12, 2)    # element address
        _dd[2] = 0x0d                       # access, expect, full
        _dd[4] = 55                         # additional sense code
        _dd[5] = 56                         # additional sense code qualifier
        _dd[9] = 0xca                       # svalid, invert, ed medium-type==2
        _dd[10:12] = scsi_int_to_ba(27, 2)  # storage element address
        _d += _dd

        _d[2:4] = scsi_int_to_ba(len(_dd), 2)
        _d[5:8] = scsi_int_to_ba(1 * len(_dd), 3)
        data += _d

        # second element status page, containing two elements
        _d = bytearray(8)
        _d[0] = READELEMENTSTATUS.ELEMENT_TYPE.DATA_TRANSFER
        _d[1] = 0x00

        # first element
        _dd = bytearray(12 + 4)
        _dd[0:2] = scsi_int_to_ba(13, 2)    # element address
        _dd[2] = 0x0c                       # access, expect
        _dd[4] = 55                         # additional sense code
        _dd[5] = 56                         # additional sense code qualifier
        _dd[9] = 0xcf                       # svalid, invert, ed medium-type==7
        _dd[10:12] = scsi_int_to_ba(28, 2)  # storage element address
        _d += _dd

        # second element
        _dd = bytearray(12 + 4)
        _dd[0:2] = scsi_int_to_ba(14, 2)    # element address
        _dd[2] = 0x08                       # access
        _dd[4] = 55                         # additional sense code
        _dd[5] = 56                         # additional sense code qualifier
        _dd[9] = 0x86                       # svalid, medium-type==6
        _dd[10:12] = scsi_int_to_ba(29, 2)  # storage element address
        _d += _dd

        _d[2:4] = scsi_int_to_ba(len(_dd), 2)
        _d[5:8] = scsi_int_to_ba(2 * len(_dd), 3)
        data += _d

        data[5:8] = scsi_int_to_ba(len(data) - 8, 3)
        cmd.datain[:len(data)] = data[:]

class UnmarshallReadelementstatusTest(unittest.TestCase):
    def test_main(self):
        with MockSCSI(MockReadElementStatus(smc)) as s:
            i = s.readelementstatus(300, 700, element_type=READELEMENTSTATUS.ELEMENT_TYPE.STORAGE, voltag=1, curdata=1,
                                    dvcid=1).result
            self.assertEqual(i['first_element_address'], 12)
            self.assertEqual(i['num_elements'], 3)

            self.assertEqual(len(i['element_status_pages']), 2)

            page = i['element_status_pages'][0]
            self.assertEqual(page['element_type'], 2)
            self.assertEqual(page['pvoltag'], 0)
            self.assertEqual(page['avoltag'], 0)
            self.assertEqual(len(page['element_descriptors']), 1)
            self.assertEqual(page['element_descriptors'][0]['element_address'], 12)
            self.assertEqual(page['element_descriptors'][0]['access'], 1)
            self.assertEqual(page['element_descriptors'][0]['except'], 1)
            self.assertEqual(page['element_descriptors'][0]['full'], 1)
            self.assertEqual(page['element_descriptors'][0]['additional_sense_code'], 55)
            self.assertEqual(page['element_descriptors'][0]['additional_sense_code_qualifier'], 56)
            self.assertEqual(page['element_descriptors'][0]['svalid'], 1)
            self.assertEqual(page['element_descriptors'][0]['invert'], 1)
            self.assertEqual(page['element_descriptors'][0]['ed'], 1)
            self.assertEqual(page['element_descriptors'][0]['medium_type'], 2)
            self.assertEqual(page['element_descriptors'][0]['source_storage_element_address'], 27)

            page = i['element_status_pages'][1]
            self.assertEqual(page['element_type'], 4)
            self.assertEqual(page['pvoltag'], 0)
            self.assertEqual(page['avoltag'], 0)
            self.assertEqual(len(page['element_descriptors']), 2)
            self.assertEqual(page['element_descriptors'][0]['element_address'], 13)
            self.assertEqual(page['element_descriptors'][0]['access'], 1)
            self.assertEqual(page['element_descriptors'][0]['except'], 1)
            self.assertEqual(page['element_descriptors'][0]['full'], 0)
            self.assertEqual(page['element_descriptors'][0]['additional_sense_code'], 55)
            self.assertEqual(page['element_descriptors'][0]['additional_sense_code_qualifier'], 56)
            self.assertEqual(page['element_descriptors'][0]['svalid'], 1)
            self.assertEqual(page['element_descriptors'][0]['invert'], 1)
            self.assertEqual(page['element_descriptors'][0]['ed'], 1)
            self.assertEqual(page['element_descriptors'][0]['medium_type'], 7)
            self.assertEqual(page['element_descriptors'][0]['source_storage_element_address'], 28)

            self.assertEqual(page['element_descriptors'][1]['element_address'], 14)
            self.assertEqual(page['element_descriptors'][1]['access'], 1)
            self.assertEqual(page['element_descriptors'][1]['except'], 0)
            self.assertEqual(page['element_descriptors'][1]['full'], 0)
            self.assertEqual(page['element_descriptors'][1]['additional_sense_code'], 55)
            self.assertEqual(page['element_descriptors'][1]['additional_sense_code_qualifier'], 56)
            self.assertEqual(page['element_descriptors'][1]['svalid'], 1)
            self.assertEqual(page['element_descriptors'][1]['invert'], 0)
            self.assertEqual(page['element_descriptors'][1]['ed'], 0)
            self.assertEqual(page['element_descriptors'][1]['medium_type'], 6)
            self.assertEqual(page['element_descriptors'][1]['source_storage_element_address'], 29)

            d = ReadElementStatus.unmarshall_datain(ReadElementStatus.marshall_datain(i))
            self.assertEqual(d, i)

if __name__ == '__main__':
    unittest.main()
