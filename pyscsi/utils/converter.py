# coding: utf-8

# Copyright:
#  Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
#  Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
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


from __future__ import print_function


def scsi_int_to_ba(to_convert=0, array_size=4):
    """
    This function converts a  integer of (8 *array_size)-bit to a bytearray(array_size) in
    BigEndian byte order. Here we use the 32-bit as default.

    example:

        >>scsi_to_ba(34,4)
        bytearray(b'\x00\x00\x00"')

        so we take a 32-bit integer and get a byte array(4)

    :to_convert: a integer
    :array_size: a integer defining the size of the byte array
    :return: a byte array
    """
    return bytearray((to_convert >> i * 8) & 0xff for i in reversed(range(array_size)))


def scsi_ba_to_int(ba):
    """
    This function converts a bytearray  in BigEndian byte order
    to an integer.

    param ba: a bytearray
    return: an integer
    """
    return sum(ba[i] << ((len(ba) - 1 - i) * 8) for i in range(len(ba)))


def decode_bits(data, check_dict, result_dict):
    """
    helper method to perform some simple bit operations

    the list in the value of each key:value pair contains 2 values
    - the bit mask
    - thy byte number for the byte in the datain byte array

    for now we assume he have to right shift only

    :data: a buffer containing the bits to decode
    :check_dict: a dict with a list as value in each key:value pair
    """
    for key in check_dict.keys():
        # get the values from dict
        bitmask, byte_pos = check_dict[key]
        _num = 1
        _bm = bitmask
        while _bm > 0xff:
            _bm >>= 8
            _num += 1
        value = scsi_ba_to_int(data[byte_pos:byte_pos + _num])
        while not bitmask & 0x01:
            bitmask >>= 1
            value >>= 1
        value &= bitmask
        result_dict.update({key: value})


def encode_dict(data_dict, check_dict, result):
    """
    encode a dict back into a bytearray
    """
    for key in data_dict.keys():
        if not key in check_dict:
            continue
        value = data_dict[key]
        bitmask, bytepos = check_dict[key]

        _num = 1
        _bm = bitmask
        while _bm > 0xff:
            _bm >>= 8
            _num += 1

        _bm = bitmask
        while not _bm & 0x01:
            _bm >>= 1
            value <<= 1

        v = scsi_int_to_ba(value, _num)
        for i in range(len(v)):
            result[bytepos + i] ^= v[i]


def print_data(data_dict):
    """
    A small method to print out data we generate in this package.

    It's not really a converter but in a way we convert a dict of
    key - value pairs into strings ...

    :param data_dict: a dictionary
    :return: a few strings
    """
    for k, v in data_dict.items():
        if isinstance(v, dict):
            print(k)
            print_data(v)
        else:
            if isinstance(v, basestring):
                print('%s -> %s' % (k, v))
            elif isinstance(v, float):
                print('%s -> %.02d' % (k, v))
            else:
                print('%s -> 0x%02X' % (k, v))