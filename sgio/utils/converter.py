# coding: utf-8

#      Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
#
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU Lesser General Public License as published by
#	   the Free Software Foundation; either version 2.1 of the License, or
#	   (at your option) any later version.
#
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU Lesser General Public License for more details.
#
#	   You should have received a copy of the GNU Lesser General Public License
#	   along with this program; if not, see <http://www.gnu.org/licenses/>.


def scsi_16_to_ba(i):
    """
    This function converts a 16-bit integer to a bytearray(2) in
    BigEndian byte order.

    i: a 16-bit integer
    return: a bytearray(2)
    """
    ba = bytearray(2)
    ba[0] = (i >> 8) & 0xff
    ba[1] = i & 0xff
    return ba


def scsi_32_to_ba(i):
    """
    This function converts a 32-bit integer to a bytearray(4) in
    BigEndian byte order.

    i: a 32-bit integer
    return: a bytearray(4)
    """
    ba = bytearray(4)
    ba[0] = (i >> 24) & 0xff
    ba[1] = (i >> 16) & 0xff
    ba[2] = (i >> 8) & 0xff
    ba[3] = i & 0xff
    return ba


def scsi_64_to_ba(i):
    """
    This function converts a 64-bit integer to a bytearray(8) in
    BigEndian byte order.

    i: a 64-bit integer
    return: a bytearray(8)
    """
    ba = bytearray(8)
    ba[0] = (i >> 56) & 0xff
    ba[1] = (i >> 48) & 0xff
    ba[2] = (i >> 40) & 0xff
    ba[3] = (i >> 32) & 0xff
    ba[4] = (i >> 24) & 0xff
    ba[5] = (i >> 16) & 0xff
    ba[6] = (i >> 8) & 0xff
    ba[7] = i & 0xff
    return ba
