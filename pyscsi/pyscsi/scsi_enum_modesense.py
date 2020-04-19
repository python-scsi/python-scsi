# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

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
__all__ = ['PC', 'PAGE_CODE', 'MODESENSE6', 'MODESENSE10']
# ------------------------------------------------------------------------------
# Mode page bits dictionaries
#------------------------------------------------------------------------------

# cdb definition for mode
modesense6_cdb_bits = {'opcode': [0xff, 0],
                        'dbd': [0x08, 1],
                        'pc': [0xc0, 2],
                        'page_code': [0x3f, 2],
                        'sub_page_code': [0xff, 3],
                        'alloc_len': [0xff, 4], }

modeselect6_cdb_bits = {'opcode': [0xff, 0],
                        'pf': [0x10, 1],
                        'sp': [0x01, 1],
                        'parameter_list_length': [0xff, 4], }

# mode parameter header definition
mode_parameter_header6_bits = {'medium_type': [0xff, 1],
                              'device_specific_parameter': [0xff, 2], }

mode_parameter_header10_bits = {'medium_type': [0xff, 2],
                              'device_specific_parameter': [0xff, 3],
                              'longlba': [0x01, 4], }

# other mode page bit definitions
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

power_condition_bits = {'pm_bg_precedence': [0xc0, 2],
                        'standby_y': [0x01, 1],
                        'idle_c': [0x08, 3],
                        'idle_b': [0x04, 3],
                        'idle_a': [0x02, 3],
                        'standby_z': [0x01, 2],
                        'idle_a_condition_timer': [0xffffffff, 4],      # byte 4 to 7
                        'idle_b_condition_timer': [0xffffffff, 12],     # byte 12 to 15
                        'idle_c_condition_timer': [0xffffffff, 16],     # byte 16 to 19
                        'standby_y_condition_timer': [0xffffffff, 20],  # byte 20 to 23
                        'standby_z_condition_timer': [0xffffffff, 8],   # byte 8 to 11
                        'ccf_idle': [0xc0, 39],
                        'ccf_standby': [0x30, 39],
                        'ccf_stopped': [0x0c, 39], }

power_consumption_bits = {'POWER_CONSUMPTION_IDENTIFIER': [0xff, 7], }

protocol_specific_logical_unit_bits = {'protocol_specific_mode_parameters': [0xf0, 2],
                                       'protocol_identifier': [0x0f, 2], }

# mode page definitions
modepage6bits = {'mode_parameter_header_bits': mode_parameter_header6_bits,
                 'page_zero_bits': page_zero_bits,
                 'sub_page_bits': sub_page_bits,
                 'element_address_bits': element_address_bits,
                 'control_bits': control_bits,
                 'control_extension_1_bits': control_extension_1_bits,
                 'power_condition_bits': power_condition_bits,
                 'power_consumption_bits': power_consumption_bits,
                 'disconnect_reconnect_bits': disconnect_reconnect_bits, }

modepage10bits = {'mode_parameter_header_bits': mode_parameter_header10_bits,
                  'page_zero_bits': page_zero_bits,
                  'sub_page_bits': sub_page_bits,
                  'element_address_bits': element_address_bits,
                  'control_bits': control_bits,
                  'control_extension_1_bits': control_extension_1_bits,
                  'power_condition_bits': power_condition_bits,
                  'power_consumption_bits': power_consumption_bits,
                  'disconnect_reconnect_bits': disconnect_reconnect_bits, }

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
MODESENSE6 = Enum(modepage6bits)
MODESENSE10 = Enum(modepage10bits)
