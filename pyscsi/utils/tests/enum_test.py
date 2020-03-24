# Copyright:
#  Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
#  Copyright (C) 2015 by Markus Rosjat <markus.rosjat@gmail.com>
#  Copyright (C) 2020 by Diego Elio Pettenò <flameeyes@flameeyes.com>
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

from pyscsi.utils.enum import Enum
from pyscsi.pyscsi.scsi_enum_command import smc

enum_dict = {'A': 1,
             'B': 2,
             'C': 3, }

class EnumTest(unittest.TestCase):

    def test_dict(self):
        i = Enum(enum_dict)
        assert i.A == 1
        assert i.B == 2
        assert i.C == 3
        assert i[1] == 'A'
        assert i[2] == 'B'
        assert i[3] == 'C'
        assert i[4] == ''

    def test_args(self):
        a = Enum(A=1, B=2, C=3)
        assert a.A == 1
        assert a.B == 2
        assert a.C == 3
        assert a[1] == 'A'
        assert a[2] == 'B'
        assert a[3] == 'C'
        assert a[4] == ''

    def test_defined(self):
        assert smc.WRITE_BUFFER.value == 0x3b
        assert smc.WRITE_BUFFER.name == 'WRITE_BUFFER'


if __name__ == "__main__":
    main()
