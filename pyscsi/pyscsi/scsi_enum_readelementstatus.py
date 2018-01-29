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
__all__ = ['ELEMENT_TYPE', ]

from pyscsi.utils.enum import Enum

#
# Element Type Code
#
_element_type = {'ALL': 0x00,
                 'MEDIUM_TRANSPORT': 0x01,
                 'STORAGE': 0x02,
                 'IMPORT_EXPORT': 0x03,
                 'DATA_TRANSFER': 0x04, }

ELEMENT_TYPE = Enum(_element_type)
