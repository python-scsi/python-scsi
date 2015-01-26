# coding: utf-8

# Copyright:
# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
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

from pyscsi.utils.enum import Enum


# we using Enum to utilize the mode page dict so we can use them in a more
# descriptive way. The ne enum has basically a dictionary as enum value. So we
# can access the values of the mode page bits as followed:
#
# modepage.modepagebits['bit']
#
# A mode page bit dictionary is defined as followed:
#
# mode_page_bits = { 'bit_name': [bit_mask, mode_page_byte_position], }
#
# A mode page could look like this:
#
# +-----+-------+-------+-------+--------+-------+-------+-------+--------+
# |  bit|   7   |   6   |   5   |   4    |   3   |   2   |   1   |   0    |
# |byte |       |       |       |        |       |       |       |        |
# +-----+-------+-------+-------+--------+-------+-------+-------+--------+
# |  0  |  PS   |SPF(0b)|          PAGE CODE(0Ah)                         |
# +-----+-------+-------+-------------------------------------------------+
# |  1  |                          PAGE LENGTH(0Ah)                       |
# +-----+-----------------------+--------+-------+-------+-------+--------+
# |  2  |        TST            |TMF_ONLY| DPICZ |D_SENSE| GLTSD | RLEC   |
# +-----+-----------------------+--------+-------+-------+-------+--------+
# |  3  |  QUEUE ALGORITHM MODIFIER      | NUAR  |     QERR      |obsolete|
# +-----+-------+-------+----------------+-------+---------------+--------+
# |  4  |   VS  |  RAC  | UA_INTLCK_CTRL |  SWP  |    obsolete            |
# +-----+-------+-------+-------+--------+-------+------------------------+
# |  5  |  ATO  |  TAS  | ATMPE |  RWWP  |Reserve|    AUTOLOAD MODE       |
# +-----+-------+-------+-------+--------+-------+------------------------+
# |  6  |                                                                 |
# +-----+-----------                obsolete                   -----------+
# |  7  |                                                                 |
# +-----+-----------------------------------------------------------------+
# |  8  | (MSB)                                                           |
# +-----+-----------            BUSY TIMEOUT PERIOD            -----------+
# |  9  |                                                         (LSB)   |
# +-----+-----------------------------------------------------------------+
# | 10  | (MSB)                                                           |
# +-----+-----------    EXTENDED SELF-TEST COMPLETION TIME     -----------+
# | 11  |                                                         (LSB)   |
# +-----+-----------------------------------------------------------------+
#
# So part of the resulting dict should look like this:
#
# mode_page_bits = { 'swp': [0x08, 4],}
#

# ------------------------------------------------------------------------------
# Mode page bits dictionaries
#------------------------------------------------------------------------------
cdb_bits = {'opcode': [0xff, 0],
            'dbd': [0x08, 1],
            'pc': [0xc0, 2],
            'page_code': [0x3f, 2],
            'sub_page_code': [0xff, 3],
            'alloc_len': [0xff, 4], }

modeselect6_cdb_bits = {'opcode': [0xff, 0],
                        'pf': [0x10, 1],
                        'sp': [0x01, 1],
                        'parameter_list_length': [0xff, 4], }

mode_parameter_header_bits = {'medium_type': [0xff, 1],
                              'device_specific_parameter': [0xff, 2], }

page_zero_bits = {'ps': [0x80, 0],
                  'spf': [0x40, 0],
                  'page_code': [0x3f, 0], }

sub_page_bits = {'ps': [0x80, 0],
                 'spf': [0x40, 0],
                 'page_code': [0x3f, 0],
                 'sub_page_code': [0xff, 1], }

element_address_bits = {'first_medium_transport_element_address': [0xffff, 0],
                        'num_medium_transport_elements': [0xffff, 2],
                        'first_storage_element_address': [0xffff, 4],
                        'num_storage_elements': [0xffff, 6],
                        'first_import_element_address': [0xffff, 8],
                        'num_import_elements': [0xffff, 10],
                        'first_data_transfer_element_address': [0xffff, 12],
                        'num_data_transfer_elements': [0xffff, 14], }

control_bits = {'tst': [0xe0, 0],
                'tmf_only': [0x10, 0],
                'dpicz': [0x08, 0],
                'd_sense': [0x04, 0],
                'gltsd': [0x02, 0],
                'rlec': [0x01, 0],
                'queue_algorithm_modifier': [0xf0, 1],
                'nuar': [0x08, 1],
                'qerr': [0x06, 1],
                'vs': [0x80, 2],
                'rac': [0x40, 2],
                'ua_intlck_ctrl': [0x30, 2],
                'swp': [0x08, 2],
                'ato': [0x80, 3],
                'tas': [0x40, 3],
                'atmpe': [0x20, 3],
                'rwwp': [0x10, 3],
                'autoload_mode': [0x07, 3],
                'busy_timeout_period': [0xffff, 6],
                'extended_self_test_completion_time': [0xffff, 8], }

control_extension_1_bits = {'tcmos': [0x04, 0],
                            'scsip': [0x02, 0],
                            'ialuae': [0x01, 0],
                            'initial_command_priority': [0x0f, 1],
                            'maximum_sense_data_length': [0xff, 2], }

disconnect_reconnect_bits = {'buffer_full_ratio': [0xff, 0],
                             'buffer_empty_ratio': [0xff, 1],
                             'bus_inactivity_limit': [0xffff, 2],
                             'disconnect_time_limit': [0xffff, 4],
                             'connect_time_limit': [0xffff, 6],
                             'maximum_burst_size': [0xffff, 8],
                             'emdp': [0x80, 10],
                             'fair_arbitration': [0x70, 10],
                             'dimm': [0x08, 10],
                             'dtdc': [0x07, 10],
                             'first_burst_size': [0xffff, 12], }

modepagebits = {'cdb_bits': cdb_bits,
                'mode_parameter_header_bits': mode_parameter_header_bits,
                'page_zero_bits': page_zero_bits,
                'sub_page_bits': sub_page_bits,
                'element_address_bits': element_address_bits,
                'control_bits': control_bits, }

modeselectbits = {'modeselect6_cdb_bits': modeselect6_cdb_bits, }

#------------------------------------------------------------------------------
# Page Control
#------------------------------------------------------------------------------

pc = {'CURRENT': 0x00,
      'CHANGEABLE': 0x01,
      'DEFAULT': 0x02,
      'SAVED': 0x03, }

#------------------------------------------------------------------------------
# Page Codes
#------------------------------------------------------------------------------

page_code = {'DISCONNECT_RECONNECT': 0x02,
             'CONTROL': 0x0a,
             'ELEMENT_ADDRESS_ASSIGNMENT': 0x1d, }

#------------------------------------------------------------------------------
# Instantiate the Enum Objects
#------------------------------------------------------------------------------

PC = Enum(pc)
PAGE_CODE = Enum(page_code)
MODESENSE6 = Enum(modepagebits)
MODESELECT6 = Enum(modeselectbits)
