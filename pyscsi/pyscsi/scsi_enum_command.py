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
sa_maintenance_in = {
    "REPORT_ASSIGNED_UNASSIGNED_P_EXTENT": 0x00,
    "REPORT_COMPONENT_DEVICE": 0x01,
    "REPORT_COMPONENT_DEVICE_ATTACHMENTS": 0x02,
    "REPORT_DEVICE_IDENTIFICATION": 0x07,
    "REPORT_PERIPHERAL_DEVICE": 0x03,
    "REPORT_PERIPHERAL_DEVICE_ASSOCIATIONS": 0x04,
    "REPORT_PERIPHERAL_DEVICE_COMPONENT_DEVICE_IDENTIFIER": 0x05,
    "REPORT_STATES": 0x06,
    "REPORT_SUPPORTED_CONFIGURATION_METHOD": 0x09,
    "REPORT_UNCONFIGURED_CAPACITY": 0x08,
}

"""
------------------------------------------------------------------------------
Maintenance out Service Actions Dictionaries
------------------------------------------------------------------------------
"""

sa_maintenance_out = {
    "ADD_PERIPHERAL_DEVICE_COMPONENT_DEVICE": 0x00,
    "ATTACH_TO_COMPONENT_DEVICE": 0x01,
    "BREAK_PERIPHERAL_DEVICE_COMPONENT_DEVICE": 0x07,
    "EXCHANGE_P_EXTENT": 0x02,
    "EXCHANGE_PERIPHERAL_DEVICE_COMPONENT_DEVICE": 0x03,
    "INSTRUCT_COMPONENT_DEVICE": 0x04,
    "REMOVE_PERIPHERAL_DEVICE_COMPONENT_DEVICE": 0x05,
    "SET_PERIPHERAL_DEVICE_COMPONENT_DEVICE_IDENTIFIER": 0x06,
}

"""
------------------------------------------------------------------------------
Service Actions Dictionaries for the A3 opcode
------------------------------------------------------------------------------
"""

service_actions = {
    "REPORT_DEVICE_IDENTIFIER": 0x05,
    "REPORT_ALIASES": 0x0B,
    "REPORT_PRIORITY": 0x0E,
    "REPORT_SUPPORTED_OPERATION_CODES": 0x0C,
    "REPORT_SUPPORTED_TASK_MANAGEMENT_FUNCTIONS": 0x0D,
    "REPORT_TARGET_PORT_GROUPS": 0x0A,
    "REPORT_TIMESTAMP": 0x0F,
    "REPORT_IDENTIFYING_INFORMATION": 0x05,
    "REQUEST_DATA_TRANSFER_ELEMENT_INQUIRY": 0x06,
    "CHANGE_ALIASES": 0x0B,
    "SET_DEVICE_IDENTIFIER": 0x06,
    "SET_PRIORITY": 0x0E,
    "SET_TARGET_PORT_GROUPS": 0x0A,
    "SET_TIMESTAMP": 0x0F,
    "SET_IDENTIFYING_INFORMATION": 0x06,
    "ORWRITE_32": 0x000E,
    "READ_32": 0x0009,
    "VERIFY_32": 0x000A,
    "WRITE_32": 0x000B,
    "WRITE_AND_VERIFY_32": 0x000C,
    "WRITE_SAME_32": 0x000D,
    "XDREAD_32": 0x0003,
    "XDWRITE_32": 0x0004,
    "XDWRITEREAD_32": 0x0007,
    "XPWRITE_32": 0x0006,
    "GET_LBA_STATUS": 0x12,
    "READ_CAPACITY_16": 0x10,
    "REPORT_REFERRALS": 0x13,
    "OPEN_IMPORTEXPORT_ELEMENT": 0x00,
    "CLOSE_IMPORTEXPORT_ELEMENT": 0x01,
}

"""
------------------------------------------------------------------------------
Persistent Reserve In Service Actions
------------------------------------------------------------------------------
"""
sa_persistent_reserve_in = {
    "READ_KEYS": 0x00,
    "READ_RESERVATION": 0x01,
    "REPORT_CAPABILITIES": 0x02,
    "READ_FULL_STATUS": 0x03,
}

"""
------------------------------------------------------------------------------
Persistent Reserve Out Service Actions
------------------------------------------------------------------------------
"""
sa_persistent_reserve_out = {
    "REGISTER": 0x00,
    "RESERVE": 0x01,
    "RELEASE": 0x02,
    "CLEAR": 0x03,
    "PREEMPT": 0x04,
    "PREEMPT_AND_ABORT": 0x05,
    "REGISTER_AND_IGNORE_EXISTING_KEY": 0x06,
    "REGISTER_AND_MOVE": 0x07,
    "REPLACE_LOST_REGISTRATION": 0x08,
}

"""
------------------------------------------------------------------------------
opcode Dictionaries
------------------------------------------------------------------------------
"""

spc_opcodes = {
    "SPC_OPCODE_A4": OpCode("SPC_OPCODE_A4", 0xA4, service_actions),
    "SPC_OPCODE_A3": OpCode("SPC_OPCODE_A3", 0xA3, service_actions),
    "ACCESS_CONTROL_IN": OpCode("ACCESS_CONTROL_IN", 0x86, {}),
    "ACCESS_CONTROL_OUT": OpCode("ACCESS_CONTROL_OUT", 0x87, {}),
    "EXTENDED_COPY": OpCode("EXTENDED_COPY", 0x83, {}),
    "INQUIRY": OpCode("INQUIRY", 0x12, {}),
    "LOG_SELECT": OpCode("LOG_SELECT", 0x4C, {}),
    "LOG_SENSE": OpCode("LOG_SENSE", 0x4D, {}),
    "MODE_SELECT_6": OpCode("MODE_SELECT_6", 0x15, {}),
    "MODE_SELECT_10": OpCode("MODE_SELECT_10", 0x55, {}),
    "MODE_SENSE_6": OpCode("MODE_SENSE_6", 0x1A, {}),
    "MODE_SENSE_10": OpCode("MODE_SENSE_10", 0x5A, {}),
    "PERSISTENT_RESERVE_IN": OpCode(
        "PERSISTENT_RESERVE_IN", 0x5E, sa_persistent_reserve_in
    ),
    "PERSISTENT_RESERVE_OUT": OpCode(
        "PERSISTENT_RESERVE_OUT", 0x5F, sa_persistent_reserve_out
    ),
    "PREVENT_ALLOW_MEDIUM_REMOVAL": OpCode("PREVENT_ALLOW_MEDIUM_REMOVAL", 0x1E, {}),
    "READ_ATTRIBUTE": OpCode("READ_ATTRIBUTE", 0x8C, {}),
    "READ_BUFFER_10": OpCode("READ_BUFFER_10", 0x3C, {}),
    "READ_BUFFER_16": OpCode("READ_BUFFER_16", 0x9B, {}),
    "READ_MEDIA_SERIAL_NUMBER": OpCode(
        "READ_MEDIA_SERIAL_NUMBER",
        0xAB,
        {
            "READ_MEDIA_SERIAL_NUMBER": 0x01,
        },
    ),
    "RECEIVE_COPY_RESULTS": OpCode("RECEIVE_COPY_RESULTS", 0x84, {}),
    "RECEIVE_DIAGNOSTIC_RESULTS": OpCode("RECEIVE_DIAGNOSTIC_RESULTS", 0x1C, {}),
    "REPORT_LUNS": OpCode("REPORT_LUNS", 0xA0, {}),
    "REQUEST_SENSE": OpCode("REQUEST_SENSE", 0x03, {}),
    "SEND_DIAGNOSTIC": OpCode("SEND_DIAGNOSTIC", 0x1D, {}),
    "TEST_UNIT_READY": OpCode("TEST_UNIT_READY", 0x00, {}),
    "WRITE_ATTRIBUTE": OpCode("WRITE_ATTRIBUTE", 0x8D, {}),
    "WRITE_BUFFER": OpCode("WRITE_BUFFER", 0x3B, {}),
}

sbc_opcodes = {
    "SBC_OPCODE_7F": OpCode("SBC_OPCODE_7F", 0x7F, service_actions),
    "SBC_OPCODE_A4": OpCode("SBC_OPCODE_A4", 0xA4, service_actions),
    "SBC_OPCODE_A3": OpCode("SBC_OPCODE_A3", 0xA3, service_actions),
    "SBC_OPCODE_9E": OpCode("SBC_OPCODE_9E", 0x9E, service_actions),
    "ACCESS_CONTROL_IN": OpCode("ACCESS_CONTROL_IN", 0x86, {}),
    "ACCESS_CONTROL_OUT": OpCode("ACCESS_CONTROL_OUT", 0x87, {}),
    "ATA_PASS_THROUGH_12": OpCode("ATA_PASS_THROUGH_12", 0xA1, {}),
    "ATA_PASS_THROUGH_16": OpCode("ATA_PASS_THROUGH_16", 0x85, {}),
    "COMPARE_AND_WRITE": OpCode("COMPARE_AND_WRITE", 0x89, {}),
    "EXTENDED_COPY": OpCode("EXTENDED_COPY", 0x83, {}),
    "FORMAT_UNIT": OpCode("FORMAT_UNIT", 0x04, {}),
    "INQUIRY": OpCode("INQUIRY", 0x12, {}),
    "LOG_SELECT": OpCode("LOG_SELECT", 0x4C, {}),
    "LOG_SENSE": OpCode("LOG_SENSE", 0x4D, {}),
    "MAINTENANCE_IN": OpCode("MAINTENANCE_IN", 0xA3, sa_maintenance_in),
    "MAINTENANCE_OUT": OpCode("MAINTENANCE_OUT", 0xA4, sa_maintenance_out),
    "MODE_SELECT_6": OpCode("MODE_SELECT_6", 0x15, {}),
    "MODE_SELECT_10": OpCode("MODE_SELECT_10", 0x55, {}),
    "MODE_SENSE_6": OpCode("MODE_SENSE_6", 0x1A, {}),
    "MODE_SENSE_10": OpCode("MODE_SENSE_10", 0x5A, {}),
    "ORWRITE_16": OpCode("ORWRITE_16", 0x8B, {}),
    "PERSISTENT_RESERVE_IN": OpCode(
        "PERSISTENT_RESERVE_IN", 0x5E, sa_persistent_reserve_in
    ),
    "PERSISTENT_RESERVE_OUT": OpCode(
        "PERSISTENT_RESERVE_OUT", 0x5F, sa_persistent_reserve_out
    ),
    "PRE_FETCH_10": OpCode("PRE_FETCH_10", 0x34, {}),
    "PRE_FETCH_16": OpCode("PRE_FETCH_16", 0x90, {}),
    "PREVENT_ALLOW_MEDIUM_REMOVAL": OpCode("PREVENT_ALLOW_MEDIUM_REMOVAL", 0x1E, {}),
    "READ_6": OpCode("READ_6", 0x08, {}),
    "READ_10": OpCode("READ_10", 0x28, {}),
    "READ_12": OpCode("READ_12", 0xA8, {}),
    "READ_16": OpCode("READ_16", 0x88, {}),
    "READ_ATTRIBUTE": OpCode("READ_ATTRIBUTE", 0x8C, {}),
    "READ_BUFFER_10": OpCode("READ_BUFFER_10", 0x3C, {}),
    "READ_BUFFER_16": OpCode("READ_BUFFER_16", 0x9B, {}),
    "READ_CAPACITY_10": OpCode("READ_CAPACITY_10", 0x25, {}),
    "READ_DEFECT_DATA_10": OpCode("READ_DEFECT_DATA_10", 0x37, {}),
    "READ_DEFECT_DATA_12": OpCode("READ_DEFECT_DATA_12", 0xB7, {}),
    "READ_LONG_10": OpCode("READ_LONG_10", 0x3E, {}),
    "READ_LONG_16": OpCode(
        "READ_LONG_16",
        0x9E,
        {
            "READ_LONG_16": 0x11,
        },
    ),
    "REASSIGN_BLOCKS": OpCode("REASSIGN_BLOCKS", 0x07, {}),
    "RECEIVE_COPY_RESULTS": OpCode("RECEIVE_COPY_RESULTS", 0x84, {}),
    "RECEIVE_DIAGNOSTIC_RESULTS": OpCode("RECEIVE_DIAGNOSTIC_RESULTS", 0x1C, {}),
    "REDUNDANCY_GROUP_IN": OpCode("REDUNDANCY_GROUP_IN", 0xBA, {}),
    "REDUNDANCY_GROUP_OUT": OpCode("REDUNDANCY_GROUP_OT", 0xBB, {}),
    "REPORT_LUNS": OpCode("REPORT_LUNS", 0xA0, {}),
    "REQUEST_SENSE": OpCode("REQUEST_SENSE", 0x03, {}),
    "SECURITY_PROTOCOL_IN": OpCode("SECURITY_PROTOCOL_IN", 0xA2, {}),
    "SECURITY_PROTOCOL_OUT": OpCode("SECURITY_PROTOCOL_OUT", 0xB5, {}),
    "SEND_DIAGNOSTIC": OpCode("SEND_DIAGNOSTIC", 0x1D, {}),
    "SPARE_IN": OpCode("SPARE_IN", 0xBC, {}),
    "SPARE_OUT": OpCode("SPARE_OUT", 0xBD, {}),
    "START_STOP_UNIT": OpCode("START_STOP_UNIT", 0x1B, {}),
    "SYNCHRONIZE_CACHE_10": OpCode("SYNCHRONIZE_CACHE_10", 0x35, {}),
    "SYNCHRONIZE_CACHE_16": OpCode("SYNCHRONIZE_CACHE_16", 0x91, {}),
    "TEST_UNIT_READY": OpCode("TEST_UNIT_READY", 0x00, {}),
    "UNMAP": OpCode("UNMAP", 0x42, {}),
    "VERIFY_10": OpCode("VERIFY_10", 0x2F, {}),
    "VERIFY_12": OpCode("VERIFY_12", 0xAF, {}),
    "VERIFY_16": OpCode("VERIFY_16", 0x8F, {}),
    "VOLUME_SET_IN": OpCode("VOLUME_SET_IN", 0xBE, {}),
    "VOLUME_SET_OUT": OpCode("VOLUME_SET_IN", 0xBF, {}),
    "WRITE_6": OpCode("WRITE_6", 0xA0, {}),
    "WRITE_10": OpCode("WRITE_10", 0x2A, {}),
    "WRITE_12": OpCode("WRITE_12", 0xAA, {}),
    "WRITE_16": OpCode("WRITE_16", 0x8A, {}),
    "WRITE_AND_VERIFY_10": OpCode("WRITE_AND_VERIFY_10", 0x2E, {}),
    "WRITE_AND_VERIFY_12": OpCode("WRITE_AND_VERIFY_12", 0xAE, {}),
    "WRITE_AND_VERIFY_16": OpCode("WRITE_AND_VERIFY_16", 0x8E, {}),
    "WRITE_ATTRIBUTE": OpCode("WRITE_ATTRIBUTE", 0x8D, {}),
    "WRITE_BUFFER": OpCode("WRITE_BUFFER", 0x3B, {}),
    "WRITE_LONG_10": OpCode("WRITE_LONG_10", 0x3F, {}),
    "WRITE_LONG_16": OpCode(
        "WRITE_LONG_16",
        0x9F,
        {
            "WRITE_LONG_16": 0x11,
        },
    ),
    "WRITE_SAME_10": OpCode("WRITE_SAME_10", 0x41, {}),
    "WRITE_SAME_16": OpCode("WRITE_SAME_16", 0x93, {}),
    "XDREAD_10": OpCode("XDREAD_10", 0x52, {}),
    "XDWRITE_10": OpCode("XDWRITE_10", 0x50, {}),
    "XDWRITEREAD_10": OpCode("XDWRITEREAD_10", 0x53, {}),
    "XPWRITE_10": OpCode("XPWRITE_10", 0x51, {}),
}

ssc_opcodes = {
    "SSC_OPCODE_A4": OpCode("SSC_OPCODE_A4", 0xA4, service_actions),
    "SSC_OPCODE_A3": OpCode("SSC_OPCODE_A3", 0xA3, service_actions),
    "ACCESS_CONTROL_IN": OpCode("ACCESS_CONTROL_IN", 0x86, {}),
    "ACCESS_CONTROL_OUT": OpCode("ACCESS_CONTROL_OUT", 0x87, {}),
    "ERASE_16": OpCode("ERASE_16", 0x93, {}),
    "EXTENDED_COPY": OpCode("EXTENDED_COPY", 0x83, {}),
    "FORMAT_MEDIUM": OpCode("FORMAT_MEDIUM", 0x04, {}),
    "INQUIRY": OpCode("INQUIRY", 0x12, {}),
    "LOAD_UNLOAD": OpCode("LOAD_UNLOAD", 0x1B, {}),
    "LOCATE_16": OpCode("LOCATE_16", 0x92, {}),
    "LOG_SELECT": OpCode("LOG_SELECT", 0x4C, {}),
    "LOG_SENSE": OpCode("LOG_SENSE", 0x4D, {}),
    "MODE_SELECT_6": OpCode("MODE_SELECT_6", 0x15, {}),
    "MODE_SELECT_10": OpCode("MODE_SELECT_10", 0x55, {}),
    "MODE_SENSE_6": OpCode("MODE_SENSE_6", 0x1A, {}),
    "MODE_SENSE_10": OpCode("MODE_SENSE_10", 0x5A, {}),
    "MOVE_MEDIUM_ATTACHED": OpCode("MOVE_MEDIUM_ATTACHED", 0xA7, {}),
    "PERSISTENT_RESERVE_IN": OpCode("PERSISTENT_RESERVE_IN", 0x5E, {}),
    "PERSISTENT_RESERVE_OUT": OpCode("PERSISTENT_RESERVE_OUT", 0x5F, {}),
    "PREVENT_ALLOW_MEDIUM_REMOVAL": OpCode("PREVENT_ALLOW_MEDIUM_REMOVAL", 0x1E, {}),
    "READ_6": OpCode("READ_6", 0x08, {}),
    "READ_16": OpCode("READ_16", 0x88, {}),
    "READ_ATTRIBUTE": OpCode("READ_ATTRIBUTE", 0x8C, {}),
    "READ_BLOCK_LIMITS": OpCode("READ_BLOCK_LIMITS", 0x05, {}),
    "READ_BUFFER_10": OpCode("READ_BUFFER_10", 0x3C, {}),
    "READ_BUFFER_16": OpCode("READ_BUFFER_16", 0x9B, {}),
    "READ_ELEMENT_STATUS_ATTACHED": OpCode("READ_ELEMENT_STATUS_ATTACHED", 0xB4, {}),
    "READ_POSITION": OpCode("READ_POSITION", 0x34, {}),
    "READ_REVERSE_6": OpCode("READ_REVERSE_6", 0x0F, {}),
    "READ_REVERSE_16": OpCode("READ_REVERSE_16", 0x81, {}),
    "RECEIVE_COPY_RESULTS": OpCode("RECEIVE_COPY_RESULTS", 0x84, {}),
    "RECEIVE_DIAGNOSTIC_RESULTS": OpCode("RECEIVE_DIAGNOSTIC_RESULTS", 0x1C, {}),
    "RECOVER_BUFFERED_DATA": OpCode("RECOVER_BUFFERED_DATA", 0x14, {}),
    "REPORT_ALIAS": OpCode(
        "REPORT_ALIAS",
        0xA3,
        {
            "REPORT_ALIAS": 0x0B,
        },
    ),
    "REPORT_DENSITY_SUPPORT": OpCode("REPORT_DENSITY_SUPPORT", 0x44, {}),
    "REPORT_LUNS": OpCode("REPORT_LUNS", 0xA0, {}),
    "REQUEST_SENSE": OpCode("REQUEST_SENSE", 0x03, {}),
    "REWIND": OpCode("REWIND", 0x01, {}),
    "SEND_DIAGNOSTIC": OpCode("SEND_DIAGNOSTIC", 0x1D, {}),
    "SET_CAPACITY": OpCode("SET_CAPACITY", 0x0B, {}),
    "SPACE_6": OpCode("SPACE_6", 0x11, {}),
    "SPACE_16": OpCode("SPACE_16", 0x91, {}),
    "TEST_UNIT_READY": OpCode("TEST_UNIT_READY", 0x00, {}),
    "VERIFY_6": OpCode("VERIFY_6", 0x13, {}),
    "VERIFY_16": OpCode("VERIFY_16", 0x8F, {}),
    "WRITE_6": OpCode("WRITE_6", 0x0A, {}),
    "WRITE_16": OpCode("WRITE_16", 0x8A, {}),
    "WRITE_ATTRIBUTE": OpCode("WRITE_ATTRIBUTE", 0x8D, {}),
    "WRITE_BUFFER": OpCode("WRITE_BUFFER", 0x3B, {}),
    "WRITE_FILEMARKS_6": OpCode("WRITE_FILEMARKS_6", 0x10, {}),
    "WRITE_FILEMARKS_16": OpCode("WRITE_FILEMARKS_16", 0x80, {}),
}

smc_opcodes = {
    "SMC_OPCODE_A4": OpCode("SMC_OPCODE_A4", 0xA4, service_actions),
    "SMC_OPCODE_A3": OpCode("SMC_OPCODE_A3", 0xA3, service_actions),
    "ACCESS_CONTROL_IN": OpCode("ACCESS_CONTROL_IN", 0x86, {}),
    "ACCESS_CONTROL_OUT": OpCode("ACCESS_CONTROL_OUT", 0x87, {}),
    "EXCHANGE_MEDIUM": OpCode("EXCHANGE_MEDIUM", 0xA6, {}),
    "INITIALIZE_ELEMENT_STATUS": OpCode("INITIALIZE_ELEMENT_STATUS", 0x07, {}),
    "INITIALIZE_ELEMENT_STATUS_WITH_RANGE": OpCode(
        "INITIALIZE_ELEMENT_STATUS_WITH_RANGE", 0x37, {}
    ),
    "INQUIRY": OpCode("INQUIRY", 0x12, {}),
    "LOG_SELECT": OpCode("LOG_SELECT", 0x4C, {}),
    "LOG_SENSE": OpCode("LOG_SENSE", 0x4D, {}),
    "MAINTENANCE_IN": OpCode("MAINTENANCE_IN", 0xA3, sa_maintenance_in),
    "MAINTENANCE_OUT": OpCode("MAINTENANCE_OUT", 0xA4, sa_maintenance_out),
    "MODE_SELECT_6": OpCode("MODE_SELECT_6", 0x15, {}),
    "MODE_SELECT_10": OpCode("MODE_SELECT_10", 0x55, {}),
    "MODE_SENSE_6": OpCode("MODE_SENSE_6", 0x1A, {}),
    "MODE_SENSE_10": OpCode("MODE_SENSE_10", 0x5A, {}),
    "MOVE_MEDIUM": OpCode("MOVE_MEDIUM", 0xA5, {}),
    "OPEN_CLOSE_IMPORT_EXPORT_ELEMENT": OpCode("SMC_OPCODE_1B", 0x1B, service_actions),
    "PERSISTENT_RESERVE_IN": OpCode("PERSISTENT_RESERVE_IN", 0x5E, {}),
    "PERSISTENT_RESERVE_OUT": OpCode("PERSISTENT_RESERVE_OUT", 0x5F, {}),
    "PREVENT_ALLOW_MEDIUM_REMOVAL": OpCode("PREVENT_ALLOW_MEDIUM_REMOVAL", 0x1E, {}),
    "POSITION_TO_ELEMENT": OpCode("POSITION_TO_ELEMENT", 0x2B, {}),
    "READ_ATTRIBUTE": OpCode("READ_ATTRIBUTE", 0x8C, {}),
    "READ_BUFFER_10": OpCode("READ_BUFFER_10", 0x3C, {}),
    "READ_BUFFER_16": OpCode("READ_BUFFER_16", 0x9B, {}),
    "READ_ELEMENT_STATUS": OpCode("READ_ELEMENT_STATUS", 0xB8, {}),
    "RECEIVE_DIAGNOSTIC_RESULTS": OpCode("RECEIVE_DIAGNOSTIC_RESULTS", 0x1C, {}),
    "REDUNDANCY_GROUP_IN": OpCode("REDUNDANCY_GROUP_IN", 0xBA, {}),
    "REDUNDANCY_GROUP_OUT": OpCode("REDUNDANCY_GROUP_OUT", 0xBB, {}),
    "RELEASE_6": OpCode("RELEASE_6", 0x17, {}),
    "RELEASE_10": OpCode("RELEASE_10", 0x57, {}),
    "REPORT_LUNS": OpCode("REPORT_LUNS", 0xA0, {}),
    "REPORT_VOLUME_TYPES_SUPPORTED": OpCode("REPORT_VOLUME_TYPES_SUPPORTED", 0x44, {}),
    "REQUEST_VOLUME_ELEMENT_ADDRESS": OpCode(
        "REQUEST_VOLUME_ELEMENT_ADDRESS", 0xB5, {}
    ),
    "REQUEST_SENSE": OpCode("REQUEST_SENSE", 0x03, {}),
    "RESERVE_6": OpCode("RESERVE_6", 0x16, {}),
    "RESERVE_10": OpCode("RESERVE_10", 0x56, {}),
    "SEND_DIAGNOSTIC": OpCode("SEND_DIAGNOSTIC", 0x1D, {}),
    "SEND_VOLUME_TAG": OpCode("SEND_VOLUME_TAG", 0xB6, {}),
    "SPARE_IN": OpCode("SPARE_IN", 0xBC, {}),
    "SPARE_OUT": OpCode("SPARE_OUT", 0xBD, {}),
    "TEST_UNIT_READY": OpCode("TEST_UNIT_READY", 0x00, {}),
    "VOLUME_SET_IN": OpCode("VOLUME_SET_IN", 0xBE, {}),
    "VOLUME_SET_OUT": OpCode("VOLUME_SET_OUT", 0xBF, {}),
    "WRITE_ATTRIBUTE": OpCode("WRITE_ATTRIBUTE", 0x8D, {}),
    "WRITE_BUFFER": OpCode("WRITE_BUFFER", 0x3B, {}),
}

mmc_opcodes = {
    "BLANK": OpCode("BLANK", 0xA1, {}),
    "CLOSE_TRACK_SESSION": OpCode("CLOSE_TRACK_SESSION", 0x5B, {}),
    "FORMAT_UNIT": OpCode("FORMAT_UNIT", 0x04, {}),
    "GET_CONFIGURATION": OpCode("GET_CONFIGURATION", 0x46, {}),
    "GET_EVENT_STATUS_NOTIFICATION": OpCode("GET_EVENT_STATUS_NOTIFICATION", 0x4A, {}),
    "GET_PERFORMANCE": OpCode("GET_PERFORMANCE", 0xAC, {}),
    "INQUIRY": OpCode("INQUIRY", 0x12, {}),
    "LOAD_UNLOAD_MEDIUM": OpCode("LOAD_UNLOAD_MEDIUM", 0xA6, {}),
    "MECHANISM_STATUS": OpCode("MECHANISM_STATUS", 0xBD, {}),
    "MODE_SELECT_10": OpCode("MODE_SELECT_10", 0x55, {}),
    "MODE_SENSE_10": OpCode("MODE_SENSE_10", 0xA5, {}),
    "PREVENT_ALLOW_MEDIUM_REMOVAL": OpCode("PREVENT_ALLOW_MEDIUM_REMOVAL", 0x1E, {}),
    "READ_10": OpCode("READ_10", 0x28, {}),
    "READ_12": OpCode("READ_12", 0xA8, {}),
    "READ_BUFFER_10": OpCode("READ_BUFFER_10", 0x3C, {}),
    "READ_BUFFER_16": OpCode("READ_BUFFER_16", 0x9B, {}),
    "READ_BUFFER_CAPACITY": OpCode("READ_BUFFER_CAPACITY", 0x5C, {}),
    "READ_CAPACITY": OpCode("READ_CAPACITY", 0x25, {}),
    "READ_CD": OpCode("READ_CD", 0xBE, {}),
    "READ_CD_MSF": OpCode("READ_CD_MSF", 0xB9, {}),
    "READ_DISC_INFORMATION": OpCode("READ_DISC_INFORMATION", 0x51, {}),
    "READ_DISC_STRUCTURE": OpCode("READ_DISC_STRUCTURE", 0xAD, {}),
    "READ_FORMAT_CAPACITIES": OpCode("READ_FORMAT_CAPACITIES", 0x23, {}),
    "READ_TOC_PMA_ATIP": OpCode("READ_TOC_PMA_ATIP", 0x43, {}),
    "READ_TRACK_INFORMATION": OpCode("READ_TRACK_INFORMATION", 0x52, {}),
    "REPAIR_TRACK": OpCode("REPAIR_TRACK", 0x58, {}),
    "REPORT_KEY": OpCode("REPORT_KEY", 0xA4, {}),
    "REPORT_LUNS": OpCode("REPORT_LUNS", 0xA0, {}),
    "REQUEST_SENSE": OpCode("REQUEST_SENSE", 0x03, {}),
    "RESERVE_TRACK": OpCode("RESERVE_TRACK", 0x53, {}),
    "SECURITY_PROTOCOL_IN": OpCode("SECURITY_PROTOCOL_IN", 0xA2, {}),
    "SECURITY_PROTOCOL_OUT": OpCode("SECURITY_PROTOCOL_OUT", 0xB5, {}),
    "SEEK_10": OpCode("SEEK_10", 0x2B, {}),
    "SEND_CUE_SHEET": OpCode("SEND_CUE_SHEET", 0x5D, {}),
    "SEND_DISC_STRUCTURE": OpCode("SEND_DISC_STRUCTURE", 0xBF, {}),
    "SEND_KEY": OpCode("SEND_KEY", 0xA3, {}),
    "SEND_OPC_INFORMATION": OpCode("SEND_OPC_INFORMATION", 0x54, {}),
    "SET_CD_SPEED": OpCode("SET_CD_SPEED", 0xBB, {}),
    "SET_READ_AHEAD": OpCode("SET_READ_AHEAD", 0xA7, {}),
    "SET_STREAMING": OpCode("SET_STREAMING", 0xB6, {}),
    "START_STOP_UNIT": OpCode("START_STOP_UNIT", 0x1B, {}),
    "SYNCHRONIZE_CACHE": OpCode("SYNCHRONIZE_CACHE", 0x35, {}),
    "TEST_UNIT_READY": OpCode("TEST_UNIT_READY", 0x00, {}),
    "VERIFY_10": OpCode("VERIFY_10", 0x2F, {}),
    "WRITE_10": OpCode("WRITE_10", 0x2A, {}),
    "WRITE_12": OpCode("WRITE_12", 0xAA, {}),
    "WRITE_AND_VERIFY_10": OpCode("WRITE_AND_VERIFY_10", 0x2E, {}),
    "WRITE_BUFFER": OpCode("WRITE_BUFFER", 0x3B, {}),
}

"""
------------------------------------------------------------------------------
scsi status Dictionaries
------------------------------------------------------------------------------
"""

scsi_status = {
    "GOOD": 0x00,
    "CHECK_CONDITION": 0x02,
    "CONDITIONS_MET": 0x04,
    "BUSY": 0x08,
    "RESERVATION_CONFLICT": 0x18,
    "TASK_SET_FULL": 0x28,
    "ACA_ACTIVE": 0x30,
    "TASK_ABORTED": 0x40,
    "SGIO_ERROR": 0xFF,
}

"""
------------------------------------------------------------------------------
open/close
------------------------------------------------------------------------------
"""

action_codes = {""}

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

opcodes = {
    "INQUIRY": 0x12,
    "MODE_SENSE_6": 0x1A,
    "MOVE_MEDIUM": 0xA5,
    "READ_10": 0x28,
    "READ_12": 0xA8,
    "READ_16": 0x88,
    "READ_CAPACITY_10": 0x25,
    "READ_ELEMENT_STATUS": 0xB8,
    "SERVICE_ACTION_IN": 0x9E,
    "TEST_UNIT_READY": 0x00,
    "WRITE_10": 0x2A,
    "WRITE_12": 0xAA,
    "WRITE_16": 0x8A,
    "WRITE_SAME_10": 0x41,
    "WRITE_SAME_16": 0x93,
}

OPCODE = Enum(opcodes)

service_action_ins = {
    "READ_CAPACITY_16": 0x10,
    "GET_LBA_STATUS": 0x12,
}

SERVICE_ACTION_IN = Enum(service_action_ins)

"""
------------------------------------------------------------------------------
"""
