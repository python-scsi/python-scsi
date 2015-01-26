# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
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

from pyscsi.utils.enum import Enum

#
# Page Control
#
_pc = {'CURRENT': 0x00,
       'CHANGEABLE': 0x01,
       'DEFAULT': 0x02,
       'SAVED': 0x03, }

PC = Enum(_pc)

#
# Page Codes
#

_page_code = {
    'DISCONNECT_RECONNECT': 0x02,
    'CONTROL': 0x0a,
    'ELEMENT_ADDRESS_ASSIGNMENT': 0x1d
}

PAGE_CODE = Enum(_page_code)
