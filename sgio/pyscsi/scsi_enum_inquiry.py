# coding: utf-8

from sgio.utils.enum import Enum

#
# CDB
#
cdb_bits = {
    'opcode': [0xff, 0],
    'evpd': [0x01, 1],
    'page_code': [0xff, 2],
    'alloc_len': [0xffff, 3],
}

#
# STANDARD PAGE
#
inq_std_bits = {
    'rmb': [0x80, 1],
    'version': [0xff, 2],
    'normaca': [0x20, 3],
    'hisup': [0x10, 3],
    'response_data_format': [0x0f, 3],
    'additional_length': [0xff, 4],
    'sccs': [0x80, 5],
    'acc': [0x40, 5],
    'tpgs': [0x30, 5],
    '3pc': [0x08, 5],
    'protect': [0x01, 5],
    'encserv': [0x40, 6],
    'vs': [0x20, 6],
    'multip': [0x10, 6],
    'addr16': [0x01, 6],
    'wbus16': [0x20, 7],
    'sync': [0x10, 7],
    'cmdque': [0x02, 7],
    'vs2': [0x01, 7],
    'clocking': [0x0c, 56],
    'qas': [0x02, 56],
    'ius': [0x01, 56],
}

#
# BLOCK LIMITS PAGE
#
inq_blocklimits_bits = {
    'wsnz': [0x01, 4],
    'ugavalid': [0x80, 32],
    'max_caw_len': [0xff, 5],
    'opt_xfer_len_gran': [0xffff, 6],
    'max_xfer_len': [0xffffffff, 8],
    'opt_xfer_len': [0xffffffff, 12],
    'max_pfetch_len': [0xffffffff, 16],
    'max_unmap_lba_count': [0xffffffff, 20],
    'max_unmap_bd_count': [0xffffffff, 24],
    'opt_unmap_gran': [0xffffffff, 28],
    'unmap_gran_alignment': [0xffffffff, 32],
    'max_ws_len': [0xffffffff, 36],
}

#
# BLOCK DEVICE CHARACTERISTICS PAGE
#
inq_blockdevchar_bits = {
    'wabereq': [0xc0, 7],
    'wacereq': [0x30, 7],
    'nominal_form_factor': [0x0f, 7],
    'fuab': [0x02, 8],
    'vbuls': [0x01, 8],
    'medium_rotation_rate': [0xffff, 4],
    'product_type': [0xff, 6]
}

#
# LOGICAL BLOCK PROVISIONING PAGE
#
inq_logicalblockprov_bits = {
    'threshold_exponent': [0xff, 4],
    'lbpu': [0x80, 5],
    'lpbws': [0x40, 5],
    'lbpws10': [0x20, 5],
    'lbprz': [0x04, 5],
    'anc_sup': [0x02, 5],
    'dp': [0x01, 5],
    'provisioning_type': [0x07, 6],
}

#
# Provisioning type
#
_provisioning_type = {
    'NO_PROVISIONING_REPORTED': 0x00,
    'RESOURCE_PROVISIONED': 0x01,
    'THIN_PROVISIONED': 0x02,
}

PROVISIONING_TYPE = Enum(_provisioning_type)

#
# Device qualifier
#
_qualifiers = {
    'CONNECTED': 0x00,
    'NOT_CONNECTED': 0x01,
    'NOT_CAPABLE': 0x03,
}

QUALIFIER = Enum(_qualifiers)

#
# Device type
#
_device_types = {
    'BLOCK_DEVICE': 0x00,
    'TAPE_DEVICE': 0x01,
    'PRINTER_DEVICE': 0x02,
    'PROCESSOR_DEVICE': 0x03,
    'WRITE_ONCE_DEVICE': 0x04,
    'MULTIMEDIA_DEVICE': 0x05,
    'SCANNER_DEVICE': 0x06,
    'OPTICAL_MEMORY_DEVICE': 0x07,
    'MEDIA_CHANGER_DEVICE': 0x08,
    'COMMUNICATIONS_DEVICE': 0x09,
    'STORAGE_ARRAY_CONTROLLER': 0x0c,
    'ENCLOSURE_SERVICE_DEVICE': 0x0d,
    'SIMPLIFIED_DIRECT_ACCESS_DEVICE': 0x0e,
    'OPTICAL_CARD_READER': 0x0f,
    'BRIDGE_CONTROLLER': 0x10,
    'OBJECT_STORAGE_DEVICE': 0x11,
    'AUTOMATION_DRIVE_DEVICE': 0x12,
    'SECURITY_MANAGER_DEVICE': 0x13,
    'WELL_KNOWN_LOGICAL_UNIT': 0x1e,
    'UNKNOWN_DEVICE': 0x1f,
}

DEVICE_TYPE = Enum(_device_types)

#
# Version
#
_versions = {
    'NO_STANDARD_CLAIMED': 0x00,
    'ANSI_INCITS_301_1997': 0x03,
    'SPC_2': 0x04,
    'SPC_3': 0x05,
    'SPC_4': 0x06,
}

VERSION = Enum(_versions)

#
# TargetPortalGroupSupport
#
_tpgss = {
    'NO_ASSYMETRIC_LUN_ACCESS': 0x00,
    'ONLY_IMPLICIT_ASSYMETRIC_LUN_ACCESS': 0x01,
    'ONLY_EXPLICIT_ASSYMETRIC_LUN_ACCESS': 0x02,
    'BOTH_IMPLICIT_AND_EXPLICIT_ASSYMETRIC_LUN_ACCESS': 0x03,
}

TPGS = Enum(_tpgss)

#
# Nominal Form Factor
#
_nff = {
    'NOT REPORTED': 0x00,
    '5.25': 0x01,
    '3.5': 0x02,
    '2.5': 0x03,
    '1.8': 0x04,
    'Less than 1.8': 0x05,
}

NOMINAL_FORM_FACTOR = Enum(_nff)

#
# VPD pages
#

_vpds = {
    'SUPPORTED_VPD_PAGES':                          0x00,
    'UNIT_SERIAL_NUMBER':                           0x80,
    'DEVICE_IDENTIFICATION':                        0x83,
    'SOFTWARE_INTERFACE_IDENTIFICATION':            0x84,
    'MANAGEMENT_NETWORK_ADDRESS':                   0x85,
    'EXTENDED_INQUIRY_DATA':                        0x86,
    'MODE_PAGE_POLICT':                             0x87,
    'SCSI_PORTS':                                   0x88,
    'ATA_INFORMATION':                              0x89,
    'POWER_CONDITION':                              0x8a,
    'DEVICE_CONSTITUENTS':                          0x8b,
    'CFA_PROFILE_INFORMATION':                      0x8c,
    'POWER_CONSUMPTION':                            0x8d,
    'THIRD_PARTY_COPY':                             0x8f,
    'PROTOCOL_SPECIFIC_LOGICAL_UNIT_INFORMATION':   0x90,
    'PROTOCOL_SPECIFIC_PORT_INFORMATION':           0x91,

    #
    # SBC
    #
    'BLOCK_LIMITS':                                 0xb0,
    'BLOCK_DEVICE_CHARACTERISTICS':                 0xb1,
    'LOGICAL_BLOCK_PROVISIONING':                   0xb2,
    'REFERRALS':                                    0xb3,
    'SUPPORTED_BLOCK_LENGTHS_AND_PROTECTION_TYPES': 0xb4,
    'BLOCK_DEVICE_CHARACTERISTICS_EXTENSION':       0xb5,
}

VPD = Enum(_vpds)