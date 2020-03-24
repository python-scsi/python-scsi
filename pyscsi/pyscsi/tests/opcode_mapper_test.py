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

from pyscsi.pyscsi.scsi_enum_command import spc, sbc, ssc, smc

class OpcodeMapperTest(unittest.TestCase):

    def test_base(self):
        assert spc.SPC_OPCODE_A4.value == 0xa4
        assert sbc.SBC_OPCODE_9E.value == 0x9e
        assert ssc.READ_ELEMENT_STATUS_ATTACHED.value == 0xb4
        assert smc.MAINTENANCE_IN.value == 0xa3
        assert smc.MAINTENANCE_IN.serviceaction.REPORT_DEVICE_IDENTIFICATION == 0x07


if __name__ == "__main__":
    main()
