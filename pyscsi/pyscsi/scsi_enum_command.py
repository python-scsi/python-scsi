# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_opcode import OpCode
from pyscsi.utils.enum import Enum

# Dictionaries to define service actions and there values
#
# We use a helper to connect the service actions to the corresponding opcode.as
# The OpCode object holds a Enum object with the service actions and has a value and
# a name property to access the opcode name and value.

"""
------------------------------------------------------------------------------
Maintenance in Service Actions
------------------------------------------------------------------------------
"""
sa_maintenance_in = {'REPORT_ASSIGNED_UNASSIGNED_P_EXTENT': 0x00,
                     'REPORT_COMPONENT_DEVICE': 0x01,
                     'REPORT_COMPONENT_DEVICE_ATTACHMENTS': 0x02,
                     'REPORT_DEVICE_IDENTIFICATION': 0x07,
                     'REPORT_PERIPHERAL_DEVICE': 0x03,
                     'REPORT_PERIPHERAL_DEVICE_ASSOCIATIONS': 0x04,
                     'REPORT_PERIPHERAL_DEVICE_COMPONENT_DEVICE_IDENTIFIER': 0x05,
                     'REPORT_STATES': 0x06,
                     'REPORT_SUPPORTED_CONFIGURATION_METHOD': 0x09,
                     'REPORT_UNCONFIGURED_CAPACITY': 0x08, }

"""
------------------------------------------------------------------------------
Maintenance out Service Actions Dictionaries
------------------------------------------------------------------------------
"""

sa_maintenance_out = {'ADD_PERIPHERAL_DEVICE_COMPONENT_DEVICE': 0x00,
                      'ATTACH_TO_COMPONENT_DEVICE': 0x01,
                      'BREAK_PERIPHERAL_DEVICE_COMPONENT_DEVICE': 0x07,
                      'EXCHANGE_P_EXTENT': 0x02,
                      'EXCHANGE_PERIPHERAL_DEVICE_COMPONENT_DEVICE': 0x03,
                      'INSTRUCT_COMPONENT_DEVICE': 0x04,
                      'REMOVE_PERIPHERAL_DEVICE_COMPONENT_DEVICE': 0x05,
                      'SET_PERIPHERAL_DEVICE_COMPONENT_DEVICE_IDENTIFIER': 0x06, }

"""
------------------------------------------------------------------------------
Service Actions Dictionaries for the A3 opcode
------------------------------------------------------------------------------
"""

service_actions = {'REPORT_DEVICE_IDENTIFIER': 0x05,
                   'REPORT_ALIASES': 0x0b,
                   'REPORT_PRIORITY': 0x0e,
                   'REPORT_SUPPORTED_OPERATION_CODES': 0x0c,
                   'REPORT_SUPPORTED_TASK_MANAGEMENT_FUNCTIONS': 0x0d,
                   'REPORT_TARGET_PORT_GROUPS': 0x0a,
                   'REPORT_TIMESTAMP': 0x0f,
                   'REPORT_IDENTIFYING_INFORMATION': 0x05,
                   'REQUEST_DATA_TRANSFER_ELEMENT_INQUIRY': 0x06,
                   'CHANGE_ALIASES': 0x0b,
                   'SET_DEVICE_IDENTIFIER': 0x06,
                   'SET_PRIORITY': 0x0e,
                   'SET_TARGET_PORT_GROUPS': 0x0a,
                   'SET_TIMESTAMP': 0x0f,
                   'SET_IDENTIFYING_INFORMATION': 0x06,
                   'ORWRITE_32': 0x000e,
                   'READ_32': 0x0009,
                   'VERIFY_32': 0x000a,
                   'WRITE_32': 0x000b,
                   'WRITE_AND_VERIFY_32': 0x000c,
                   'WRITE_SAME_32': 0x000d,
                   'XDREAD_32': 0x0003,
                   'XDWRITE_32': 0x0004,
                   'XDWRITEREAD_32': 0x0007,
                   'XPWRITE_32': 0x0006,
                   'GET_LBA_STATUS': 0x12,
                   'READ_CAPACITY_16': 0x10,
                   'REPORT_REFERRALS': 0x13,
                   'OPEN_IMPORTEXPORT_ELEMENT': 0x00,
                   'CLOSE_IMPORTEXPORT_ELEMENT': 0x01, }

"""
------------------------------------------------------------------------------
opcode Dictionaries
------------------------------------------------------------------------------
"""

spc_opcodes = {'SPC_OPCODE_A4': OpCode('SPC_OPCODE_A4', 0xa4, service_actions),
               'SPC_OPCODE_A3': OpCode('SPC_OPCODE_A3', 0xa3, service_actions),
               'ACCESS_CONTROL_IN': OpCode('ACCESS_CONTROL_IN', 0x86, {}),
               'ACCESS_CONTROL_OUT': OpCode('ACCESS_CONTROL_OUT', 0x87, {}),
               'EXTENDED_COPY': OpCode('EXTENDED_COPY', 0x83, {}),
               'INQUIRY': OpCode('INQUIRY', 0x12, {}),
               'LOG_SELECT': OpCode('LOG_SELECT', 0x4c, {}),
               'LOG_SENSE': OpCode('LOG_SENSE', 0x4d, {}),
               'MODE_SELECT_6': OpCode('MODE_SELECT_6', 0x15, {}),
               'MODE_SELECT_10': OpCode('MODE_SELECT_10', 0x55, {}),
               'MODE_SENSE_6': OpCode('MODE_SENSE_6', 0x1a, {}),
               'MODE_SENSE_10': OpCode('MODE_SENSE_10', 0x5a, {}),
               'PERSISTENT_RESERVE_IN': OpCode('PERSISTENT_RESERVE_IN', 0x5e, {}),
               'PERSISTENT_RESERVE_OUT': OpCode('PERSISTENT_RESERVE_OUT', 0x5f, {}),
               'PREVENT_ALLOW_MEDIUM_REMOVAL': OpCode('PREVENT_ALLOW_MEDIUM_REMOVAL', 0x1e, {}),
               'READ_ATTRIBUTE': OpCode('READ_ATTRIBUTE', 0x8c, {}),
               'READ_BUFFER_10': OpCode('READ_BUFFER_10', 0x3c, {}),
               'READ_BUFFER_16': OpCode('READ_BUFFER_16', 0x9b, {}),
               'READ_MEDIA_SERIAL_NUMBER': OpCode('READ_MEDIA_SERIAL_NUMBER', 0xab,
                                                  {'READ_MEDIA_SERIAL_NUMBER': 0x01, }),
               'RECEIVE_COPY_RESULTS': OpCode('RECEIVE_COPY_RESULTS', 0x84, {}),
               'RECEIVE_DIAGNOSTIC_RESULTS': OpCode('RECEIVE_DIAGNOSTIC_RESULTS', 0x1c, {}),
               'REPORT_LUNS': OpCode('REPORT_LUNS', 0xa0, {}),
               'REQUEST_SENSE': OpCode('REQUEST_SENSE', 0x03, {}),
               'SEND_DIAGNOSTIC': OpCode('SEND_DIAGNOSTIC', 0x1d, {}),
               'TEST_UNIT_READY': OpCode('TEST_UNIT_READY', 0x00, {}),
               'WRITE_ATTRIBUTE': OpCode('WRITE_ATTRIBUTE', 0x8d, {}),
               'WRITE_BUFFER': OpCode('WRITE_BUFFER', 0x3b, {}), }

sbc_opcodes = {'SBC_OPCODE_7F': OpCode('SBC_OPCODE_7F', 0x7f, service_actions),
               'SBC_OPCODE_A4': OpCode('SBC_OPCODE_A4', 0xa4, service_actions),
               'SBC_OPCODE_A3': OpCode('SBC_OPCODE_A3', 0xa3, service_actions),
               'SBC_OPCODE_9E': OpCode('SBC_OPCODE_9E', 0x9e, service_actions),
               'ACCESS_CONTROL_IN': OpCode('ACCESS_CONTROL_IN', 0x86, {}),
               'ACCESS_CONTROL_OUT': OpCode('ACCESS_CONTROL_OUT', 0x87, {}),
               'COMPARE_AND_WRITE': OpCode('COMPARE_AND_WRITE', 0x89, {}),
               'EXTENDED_COPY': OpCode('EXTENDED_COPY', 0x83, {}),
               'FORMAT_UNIT': OpCode('FORMAT_UNIT', 0x04, {}),
               'INQUIRY': OpCode('INQUIRY', 0x12, {}),
               'LOG_SELECT': OpCode('LOG_SELECT', 0x4c, {}),
               'LOG_SENSE': OpCode('LOG_SENSE', 0x4d, {}),
               'MAINTENANCE_IN': OpCode('MAINTENANCE_IN', 0xa3, sa_maintenance_in),
               'MAINTENANCE_OUT': OpCode('MAINTENANCE_OUT', 0xa4, sa_maintenance_out),
               'MODE_SELECT_6': OpCode('MODE_SELECT_6', 0x15, {}),
               'MODE_SELECT_10': OpCode('MODE_SELECT_10', 0x55, {}),
               'MODE_SENSE_6': OpCode('MODE_SENSE_6', 0x1a, {}),
               'MODE_SENSE_10': OpCode('MODE_SENSE_10', 0x5a, {}),
               'ORWRITE_16': OpCode('ORWRITE_16', 0x8b, {}),
               'PERSISTENT_RESERVE_IN': OpCode('PERSISTENT_RESERVE_IN', 0x5e, {}),
               'PERSISTENT_RESERVE_OUT': OpCode('PERSISTENT_RESERVE_OUT', 0x5f, {}),
               'PRE_FETCH_10': OpCode('PRE_FETCH_10', 0x34, {}),
               'PRE_FETCH_16': OpCode('PRE_FETCH_16', 0x90, {}),
               'PREVENT_ALLOW_MEDIUM_REMOVAL': OpCode('PREVENT_ALLOW_MEDIUM_REMOVAL', 0x1e, {}),
               'READ_6': OpCode('READ_6', 0x08, {}),
               'READ_10': OpCode('READ_10', 0x28, {}),
               'READ_12': OpCode('READ_12', 0xa8, {}),
               'READ_16': OpCode('READ_16', 0x88, {}),
               'READ_ATTRIBUTE': OpCode('READ_ATTRIBUTE', 0x8c, {}),
               'READ_BUFFER_10': OpCode('READ_BUFFER_10', 0x3c, {}),
               'READ_BUFFER_16': OpCode('READ_BUFFER_16', 0x9b, {}),
               'READ_CAPACITY_10': OpCode('READ_CAPACITY_10', 0x25, {}),
               'READ_DEFECT_DATA_10': OpCode('READ_DEFECT_DATA_10', 0x37, {}),
               'READ_DEFECT_DATA_12': OpCode('READ_DEFECT_DATA_12', 0xb7, {}),
               'READ_LONG_10': OpCode('READ_LONG_10', 0x3e, {}),
               'READ_LONG_16': OpCode('READ_LONG_16', 0x9e, {'READ_LONG_16': 0x11, }),
               'REASSIGN_BLOCKS': OpCode('REASSIGN_BLOCKS', 0x07, {}),
               'RECEIVE_COPY_RESULTS': OpCode('RECEIVE_COPY_RESULTS', 0x84, {}),
               'RECEIVE_DIAGNOSTIC_RESULTS': OpCode('RECEIVE_DIAGNOSTIC_RESULTS', 0x1c, {}),
               'REDUNDANCY_GROUP_IN': OpCode('REDUNDANCY_GROUP_IN', 0xba, {}),
               'REDUNDANCY_GROUP_OUT': OpCode('REDUNDANCY_GROUP_OT', 0xbb, {}),
               'REPORT_LUNS': OpCode('REPORT_LUNS', 0xa0, {}),
               'REQUEST_SENSE': OpCode('REQUEST_SENSE', 0x03, {}),
               'SECURITY_PROTOCOL_IN': OpCode('SECURITY_PROTOCOL_IN', 0xa2, {}),
               'SECURITY_PROTOCOL_OUT': OpCode('SECURITY_PROTOCOL_OUT', 0xb5, {}),
               'SEND_DIAGNOSTIC': OpCode('SEND_DIAGNOSTIC', 0x1d, {}),
               'SPARE_IN': OpCode('SPARE_IN', 0xbc, {}),
               'SPARE_OUT': OpCode('SPARE_OUT', 0xbd, {}),
               'START_STOP_UNIT': OpCode('START_STOP_UNIT', 0x1b, {}),
               'SYNCHRONIZE_CACHE_10': OpCode('SYNCHRONIZE_CACHE_10', 0x35, {}),
               'SYNCHRONIZE_CACHE_16': OpCode('SYNCHRONIZE_CACHE_16', 0x91, {}),
               'TEST_UNIT_READY': OpCode('TEST_UNIT_READY', 0x00, {}),
               'UNMAP': OpCode('UNMAP', 0x42, {}),
               'VERIFY_10': OpCode('VERIFY_10', 0x2f, {}),
               'VERIFY_12': OpCode('VERIFY_12', 0xaf, {}),
               'VERIFY_16': OpCode('VERIFY_16', 0x8f, {}),
               'VOLUME_SET_IN': OpCode('VOLUME_SET_IN', 0xbe, {}),
               'VOLUME_SET_OUT': OpCode('VOLUME_SET_IN', 0xbf, {}),
               'WRITE_6': OpCode('WRITE_6', 0xa0, {}),
               'WRITE_10': OpCode('WRITE_10', 0x2a, {}),
               'WRITE_12': OpCode('WRITE_12', 0xaa, {}),
               'WRITE_16': OpCode('WRITE_16', 0x8a, {}),
               'WRITE_AND_VERIFY_10': OpCode('WRITE_AND_VERIFY_10', 0x2e, {}),
               'WRITE_AND_VERIFY_12': OpCode('WRITE_AND_VERIFY_12', 0xae, {}),
               'WRITE_AND_VERIFY_16': OpCode('WRITE_AND_VERIFY_16', 0x8e, {}),
               'WRITE_ATTRIBUTE': OpCode('WRITE_ATTRIBUTE', 0x8d, {}),
               'WRITE_BUFFER': OpCode('WRITE_BUFFER', 0x3b, {}),
               'WRITE_LONG_10': OpCode('WRITE_LONG_10', 0x3f, {}),
               'WRITE_LONG_16': OpCode('WRITE_LONG_16', 0x9f, {'WRITE_LONG_16': 0x11, }),
               'WRITE_SAME_10': OpCode('WRITE_SAME_10', 0x41, {}),
               'WRITE_SAME_16': OpCode('WRITE_SAME_16', 0x93, {}),
               'XDREAD_10': OpCode('XDREAD_10', 0x52, {}),
               'XDWRITE_10': OpCode('XDWRITE_10', 0x50, {}),
               'XDWRITEREAD_10': OpCode('XDWRITEREAD_10', 0x53, {}),
               'XPWRITE_10': OpCode('XPWRITE_10', 0x51, {}), }

ssc_opcodes = {'SSC_OPCODE_A4': OpCode('SSC_OPCODE_A4', 0xa4, service_actions),
               'SSC_OPCODE_A3': OpCode('SSC_OPCODE_A3', 0xa3, service_actions),
               'ACCESS_CONTROL_IN': OpCode('ACCESS_CONTROL_IN', 0x86, {}),
               'ACCESS_CONTROL_OUT': OpCode('ACCESS_CONTROL_OUT', 0x87, {}),
               'ERASE_16': OpCode('ERASE_16', 0x93, {}),
               'EXTENDED_COPY': OpCode('EXTENDED_COPY', 0x83, {}),
               'FORMAT_MEDIUM': OpCode('FORMAT_MEDIUM', 0x04, {}),
               'INQUIRY': OpCode('INQUIRY', 0x12, {}),
               'LOAD_UNLOAD': OpCode('LOAD_UNLOAD', 0x1b, {}),
               'LOCATE_16': OpCode('LOCATE_16', 0x92, {}),
               'LOG_SELECT': OpCode('LOG_SELECT', 0x4c, {}),
               'LOG_SENSE': OpCode('LOG_SENSE', 0x4d, {}),
               'MODE_SELECT_6': OpCode('MODE_SELECT_6', 0x15, {}),
               'MODE_SELECT_10': OpCode('MODE_SELECT_10', 0x55, {}),
               'MODE_SENSE_6': OpCode('MODE_SENSE_6', 0x1a, {}),
               'MODE_SENSE_10': OpCode('MODE_SENSE_10', 0x5a, {}),
               'MOVE_MEDIUM_ATTACHED': OpCode('MOVE_MEDIUM_ATTACHED', 0xa7, {}),
               'PERSISTENT_RESERVE_IN': OpCode('PERSISTENT_RESERVE_IN', 0x5e, {}),
               'PERSISTENT_RESERVE_OUT': OpCode('PERSISTENT_RESERVE_OUT', 0x5f, {}),
               'PREVENT_ALLOW_MEDIUM_REMOVAL': OpCode('PREVENT_ALLOW_MEDIUM_REMOVAL', 0x1e, {}),
               'READ_6': OpCode('READ_6', 0x08, {}),
               'READ_16': OpCode('READ_16', 0x88, {}),
               'READ_ATTRIBUTE': OpCode('READ_ATTRIBUTE', 0x8c, {}),
               'READ_BLOCK_LIMITS': OpCode('READ_BLOCK_LIMITS', 0x05, {}),
               'READ_BUFFER_10': OpCode('READ_BUFFER_10', 0x3c, {}),
               'READ_BUFFER_16': OpCode('READ_BUFFER_16', 0x9b, {}),
               'READ_ELEMENT_STATUS_ATTACHED': OpCode('READ_ELEMENT_STATUS_ATTACHED', 0xb4, {}),
               'READ_POSITION': OpCode('READ_POSITION', 0x34, {}),
               'READ_REVERSE_6': OpCode('READ_REVERSE_6', 0x0f, {}),
               'READ_REVERSE_16': OpCode('READ_REVERSE_16', 0x81, {}),
               'RECEIVE_COPY_RESULTS': OpCode('RECEIVE_COPY_RESULTS', 0x84, {}),
               'RECEIVE_DIAGNOSTIC_RESULTS': OpCode('RECEIVE_DIAGNOSTIC_RESULTS', 0x1c, {}),
               'RECOVER_BUFFERED_DATA': OpCode('RECOVER_BUFFERED_DATA', 0x14, {}),
               'REPORT_ALIAS': OpCode('REPORT_ALIAS', 0xa3, {'REPORT_ALIAS': 0x0b, }),
               'REPORT_DENSITY_SUPPORT': OpCode('REPORT_DENSITY_SUPPORT', 0x44, {}),
               'REPORT_LUNS': OpCode('REPORT_LUNS', 0xa0, {}),
               'REQUEST_SENSE': OpCode('REQUEST_SENSE', 0x03, {}),
               'REWIND': OpCode('REWIND', 0x01, {}),
               'SEND_DIAGNOSTIC': OpCode('SEND_DIAGNOSTIC', 0x1d, {}),
               'SET_CAPACITY': OpCode('SET_CAPACITY', 0x0b, {}),
               'SPACE_6': OpCode('SPACE_6', 0x11, {}),
               'SPACE_16': OpCode('SPACE_16', 0x91, {}),
               'TEST_UNIT_READY': OpCode('TEST_UNIT_READY', 0x00, {}),
               'VERIFY_6': OpCode('VERIFY_6', 0x13, {}),
               'VERIFY_16': OpCode('VERIFY_16', 0x8f, {}),
               'WRITE_6': OpCode('WRITE_6', 0x0a, {}),
               'WRITE_16': OpCode('WRITE_16', 0x8a, {}),
               'WRITE_ATTRIBUTE': OpCode('WRITE_ATTRIBUTE', 0x8d, {}),
               'WRITE_BUFFER': OpCode('WRITE_BUFFER', 0x3b, {}),
               'WRITE_FILEMARKS_6': OpCode('WRITE_FILEMARKS_6', 0x10, {}),
               'WRITE_FILEMARKS_16': OpCode('WRITE_FILEMARKS_16', 0x80, {}), }

smc_opcodes = {'SMC_OPCODE_A4': OpCode('SMC_OPCODE_A4', 0xa4, service_actions),
               'SMC_OPCODE_A3': OpCode('SMC_OPCODE_A3', 0xa3, service_actions),
               'ACCESS_CONTROL_IN': OpCode('ACCESS_CONTROL_IN', 0x86, {}),
               'ACCESS_CONTROL_OUT': OpCode('ACCESS_CONTROL_OUT', 0x87, {}),
               'EXCHANGE_MEDIUM': OpCode('EXCHANGE_MEDIUM', 0xa6, {}),
               'INITIALIZE_ELEMENT_STATUS': OpCode('INITIALIZE_ELEMENT_STATUS', 0x07, {}),
               'INITIALIZE_ELEMENT_STATUS_WITH_RANGE': OpCode('INITIALIZE_ELEMENT_STATUS_WITH_RANGE', 0x37, {}),
               'INQUIRY': OpCode('INQUIRY', 0x12, {}),
               'LOG_SELECT': OpCode('LOG_SELECT', 0x4c, {}),
               'LOG_SENSE': OpCode('LOG_SENSE', 0x4d, {}),
               'MAINTENANCE_IN': OpCode('MAINTENANCE_IN', 0xa3, sa_maintenance_in),
               'MAINTENANCE_OUT': OpCode('MAINTENANCE_OUT', 0xa4, sa_maintenance_out),
               'MODE_SELECT_6': OpCode('MODE_SELECT_6', 0x15, {}),
               'MODE_SELECT_10': OpCode('MODE_SELECT_10', 0x55, {}),
               'MODE_SENSE_6': OpCode('MODE_SENSE_6', 0x1a, {}),
               'MODE_SENSE_10': OpCode('MODE_SENSE_10', 0x5a, {}),
               'MOVE_MEDIUM': OpCode('MOVE_MEDIUM', 0xa5, {}),
               'OPEN_CLOSE_IMPORT_EXPORT_ELEMENT': OpCode('SMC_OPCODE_1B', 0x1b, service_actions),
               'PERSISTENT_RESERVE_IN': OpCode('PERSISTENT_RESERVE_IN', 0x5e, {}),
               'PERSISTENT_RESERVE_OUT': OpCode('PERSISTENT_RESERVE_OUT', 0x5f, {}),
               'PREVENT_ALLOW_MEDIUM_REMOVAL': OpCode('PREVENT_ALLOW_MEDIUM_REMOVAL', 0x1e, {}),
               'POSITION_TO_ELEMENT': OpCode('POSITION_TO_ELEMENT', 0x2b, {}),
               'READ_ATTRIBUTE': OpCode('READ_ATTRIBUTE', 0x8c, {}),
               'READ_BUFFER_10': OpCode('READ_BUFFER_10', 0x3c, {}),
               'READ_BUFFER_16': OpCode('READ_BUFFER_16', 0x9b, {}),
               'READ_ELEMENT_STATUS': OpCode('READ_ELEMENT_STATUS', 0xb8, {}),
               'RECEIVE_DIAGNOSTIC_RESULTS': OpCode('RECEIVE_DIAGNOSTIC_RESULTS', 0x1c, {}),
               'REDUNDANCY_GROUP_IN': OpCode('REDUNDANCY_GROUP_IN', 0xba, {}),
               'REDUNDANCY_GROUP_OUT': OpCode('REDUNDANCY_GROUP_OUT', 0xbb, {}),
               'RELEASE_6': OpCode('RELEASE_6', 0x17, {}),
               'RELEASE_10': OpCode('RELEASE_10', 0x57, {}),
               'REPORT_LUNS': OpCode('REPORT_LUNS', 0xa0, {}),
               'REPORT_VOLUME_TYPES_SUPPORTED': OpCode('REPORT_VOLUME_TYPES_SUPPORTED', 0x44, {}),
               'REQUEST_VOLUME_ELEMENT_ADDRESS': OpCode('REQUEST_VOLUME_ELEMENT_ADDRESS', 0xb5, {}),
               'REQUEST_SENSE': OpCode('REQUEST_SENSE', 0x03, {}),
               'RESERVE_6': OpCode('RESERVE_6', 0x16, {}),
               'RESERVE_10': OpCode('RESERVE_10', 0x56, {}),
               'SEND_DIAGNOSTIC': OpCode('SEND_DIAGNOSTIC', 0x1d, {}),
               'SEND_VOLUME_TAG': OpCode('SEND_VOLUME_TAG', 0xb6, {}),
               'SPARE_IN': OpCode('SPARE_IN', 0xbc, {}),
               'SPARE_OUT': OpCode('SPARE_OUT', 0xbd, {}),
               'TEST_UNIT_READY': OpCode('TEST_UNIT_READY', 0x00, {}),
               'VOLUME_SET_IN': OpCode('VOLUME_SET_IN', 0xbe, {}),
               'VOLUME_SET_OUT': OpCode('VOLUME_SET_OUT', 0xbf, {}),
               'WRITE_ATTRIBUTE': OpCode('WRITE_ATTRIBUTE', 0x8d, {}),
               'WRITE_BUFFER': OpCode('WRITE_BUFFER', 0x3b, {}), }

mmc_opcodes = {'BLANK': OpCode('BLANK', 0xa1, {}),
               'CLOSE_TRACK_SESSION': OpCode('CLOSE_TRACK_SESSION', 0x5b, {}),
               'FORMAT_UNIT': OpCode('FORMAT_UNIT', 0x04, {}),
               'GET_CONFIGURATION': OpCode('GET_CONFIGURATION', 0x46, {}),
               'GET_EVENT_STATUS_NOTIFICATION': OpCode('GET_EVENT_STATUS_NOTIFICATION', 0x4a, {}),
               'GET_PERFORMANCE': OpCode('GET_PERFORMANCE', 0xac, {}),
               'INQUIRY': OpCode('INQUIRY', 0x12, {}),
               'LOAD_UNLOAD_MEDIUM': OpCode('LOAD_UNLOAD_MEDIUM', 0xa6, {}),
               'MECHANISM_STATUS': OpCode('MECHANISM_STATUS', 0xbd, {}),
               'MODE_SELECT_10': OpCode('MODE_SELECT_10', 0x55, {}),
               'MODE_SENSE_10': OpCode('MODE_SENSE_10', 0xa5, {}),
               'PREVENT_ALLOW_MEDIUM_REMOVAL': OpCode('PREVENT_ALLOW_MEDIUM_REMOVAL', 0x1e, {}),
               'READ_10': OpCode('READ_10', 0x28, {}),
               'READ_12': OpCode('READ_12', 0xa8, {}),
               'READ_BUFFER_10': OpCode('READ_BUFFER_10', 0x3c, {}),
               'READ_BUFFER_16': OpCode('READ_BUFFER_16', 0x9b, {}),
               'READ_BUFFER_CAPACITY': OpCode('READ_BUFFER_CAPACITY', 0x5c, {}),
               'READ_CAPACITY': OpCode('READ_CAPACITY', 0x25, {}),
               'READ_CD': OpCode('READ_CD', 0xbe, {}),
               'READ_CD_MSF': OpCode('READ_CD_MSF', 0xb9, {}),
               'READ_DISC_INFORMATION': OpCode('READ_DISC_INFORMATION', 0x51, {}),
               'READ_DISC_STRUCTURE': OpCode('READ_DISC_STRUCTURE', 0xad, {}),
               'READ_FORMAT_CAPACITIES': OpCode('READ_FORMAT_CAPACITIES', 0x23, {}),
               'READ_TOC_PMA_ATIP': OpCode('READ_TOC_PMA_ATIP', 0x43, {}),
               'READ_TRACK_INFORMATION': OpCode('READ_TRACK_INFORMATION', 0x52, {}),
               'REPAIR_TRACK': OpCode('REPAIR_TRACK', 0x58, {}),
               'REPORT_KEY': OpCode('REPORT_KEY', 0xa4, {}),
               'REPORT_LUNS': OpCode('REPORT_LUNS', 0xa0, {}),
               'REQUEST_SENSE': OpCode('REQUEST_SENSE', 0x03, {}),
               'RESERVE_TRACK': OpCode('RESERVE_TRACK', 0x53, {}),
               'SECURITY_PROTOCOL_IN': OpCode('SECURITY_PROTOCOL_IN', 0xa2, {}),
               'SECURITY_PROTOCOL_OUT': OpCode('SECURITY_PROTOCOL_OUT', 0xb5, {}),
               'SEEK_10': OpCode('SEEK_10', 0x2b, {}),
               'SEND_CUE_SHEET': OpCode('SEND_CUE_SHEET', 0x5d, {}),
               'SEND_DISC_STRUCTURE': OpCode('SEND_DISC_STRUCTURE', 0xbf, {}),
               'SEND_KEY': OpCode('SEND_KEY', 0xa3, {}),
               'SEND_OPC_INFORMATION': OpCode('SEND_OPC_INFORMATION', 0x54, {}),
               'SET_CD_SPEED': OpCode('SET_CD_SPEED', 0xbb, {}),
               'SET_READ_AHEAD': OpCode('SET_READ_AHEAD', 0xa7, {}),
               'SET_STREAMING': OpCode('SET_STREAMING', 0xb6, {}),
               'START_STOP_UNIT': OpCode('START_STOP_UNIT', 0x1b, {}),
               'SYNCHRONIZE_CACHE': OpCode('SYNCHRONIZE_CACHE', 0x35, {}),
               'TEST_UNIT_READY': OpCode('TEST_UNIT_READY', 0x00, {}),
               'VERIFY_10': OpCode('VERIFY_10', 0x2f, {}),
               'WRITE_10': OpCode('WRITE_10', 0x2a, {}),
               'WRITE_12': OpCode('WRITE_12', 0xaa, {}),
               'WRITE_AND_VERIFY_10': OpCode('WRITE_AND_VERIFY_10', 0x2e, {}),
               'WRITE_BUFFER': OpCode('WRITE_BUFFER', 0x3b, {}), }

"""
------------------------------------------------------------------------------
scsi status Dictionaries
------------------------------------------------------------------------------
"""

scsi_status = {'GOOD': 0x00,
               'CHECK_CONDITION': 0x02,
               'CONDITIONS_MET': 0x04,
               'BUSY': 0x08,
               'RESERVATION_CONFLICT': 0x18,
               'TASK_SET_FULL': 0x28,
               'ACA_ACTIVE': 0x30,
               'TASK_ABORTED': 0x40,
               'SGIO_ERROR': 0xff, }

"""
------------------------------------------------------------------------------
open/close
------------------------------------------------------------------------------
"""

action_codes = {''}

"""
------------------------------------------------------------------------------
Instantiate the Enum Objects
------------------------------------------------------------------------------
"""

SCSI_STATUS = Enum(scsi_status)

spc = Enum(spc_opcodes)
sbc = Enum(sbc_opcodes)
ssc = Enum(ssc_opcodes)
smc = Enum(smc_opcodes)
mmc = Enum(mmc_opcodes)

"""
------------------------------------------------------------------------------
Obsolete Dictionaries and Enums
------------------------------------------------------------------------------

NOTE: the dicts and Enums in this section and will be removed in a future release

"""

opcodes = {'INQUIRY': 0x12,
           'MODE_SENSE_6': 0x1a,
           'MOVE_MEDIUM': 0xa5,
           'READ_10': 0x28,
           'READ_12': 0xa8,
           'READ_16': 0x88,
           'READ_CAPACITY_10': 0x25,
           'READ_ELEMENT_STATUS': 0xb8,
           'SERVICE_ACTION_IN': 0x9e,
           'TEST_UNIT_READY': 0x00,
           'WRITE_10': 0x2a,
           'WRITE_12': 0xaa,
           'WRITE_16': 0x8a,
           'WRITE_SAME_10': 0x41,
           'WRITE_SAME_16': 0x93,
           }

OPCODE = Enum(opcodes)

service_action_ins = {'READ_CAPACITY_16': 0x10,
                      'GET_LBA_STATUS': 0x12, }

SERVICE_ACTION_IN = Enum(service_action_ins)

"""
------------------------------------------------------------------------------
"""
