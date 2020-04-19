# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.utils.enum import Enum

__all__ = ['PROVISIONING_TYPE', 'QUALIFIER', 'DEVICE_TYPE',
           'VERSION', 'TPGS', 'NOMINAL_FORM_FACTOR', 'PROTOCOL_IDENTIFIER',
           'CODE_SET', 'ASSOCIATION', 'DESIGNATOR', 'NAA', 'VPD', ]
#
# Provisioning type
#
_provisioning_type = {'NO_PROVISIONING_REPORTED': 0x00,
                      'RESOURCE_PROVISIONED': 0x01,
                      'THIN_PROVISIONED': 0x02, }

PROVISIONING_TYPE = Enum(_provisioning_type)

#
# Device qualifier
#
_qualifiers = {'CONNECTED': 0x00,
               'NOT_CONNECTED': 0x01,
               'NOT_CAPABLE': 0x03, }

QUALIFIER = Enum(_qualifiers)

#
# Device type
#
_device_types = {'BLOCK_DEVICE': 0x00,
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
                 'UNKNOWN_DEVICE': 0x1f, }

DEVICE_TYPE = Enum(_device_types)

#
# Version
#
_versions = {'NO_STANDARD_CLAIMED': 0x00,
             'ANSI_INCITS_301_1997': 0x03,
             'SPC_2': 0x04,
             'SPC_3': 0x05,
             'SPC_4': 0x06, }

VERSION = Enum(_versions)

#
# TargetPortalGroupSupport
#
_tpgss = {'NO_ASSYMETRIC_LUN_ACCESS': 0x00,
          'ONLY_IMPLICIT_ASSYMETRIC_LUN_ACCESS': 0x01,
          'ONLY_EXPLICIT_ASSYMETRIC_LUN_ACCESS': 0x02,
          'BOTH_IMPLICIT_AND_EXPLICIT_ASSYMETRIC_LUN_ACCESS': 0x03, }

TPGS = Enum(_tpgss)

#
# Nominal Form Factor
#
_nff = {'NOT REPORTED': 0x00,
        '5.25': 0x01,
        '3.5': 0x02,
        '2.5': 0x03,
        '1.8': 0x04,
        'Less than 1.8': 0x05, }

NOMINAL_FORM_FACTOR = Enum(_nff)

_protocol_identifier = {'FIBRE_CHANNEL': 0x00,
                        'SCSI_PARALLEL_INTERFACE': 0x01,
                        'SERIAL_STORAGE_ARCHITECTURE': 0x02,
                        'SERIAL_BUS_PROTOCOL': 0x03,
                        'RDMA': 0x04,
                        'ISCSI': 0x05,
                        'SAS': 0x06,
                        'AUTOMATION_DRIVE_INTERFACE': 0x07,
                        'AT_ATTACHMENT_INTERFACE': 0x08,
                        'USB_ATTACHED_SCSI': 0x09,
                        'SCSI_OVER_PCI_EXPRESS': 0x0a,
                        'NO_SPECIFIC_PROTOCOL': 0x0f, }

PROTOCOL_IDENTIFIER = Enum(_protocol_identifier)

_code_set = {'BINARY': 0x01,
             'ASCII': 0x02,
             'UTF8': 0x03, }

CODE_SET = Enum(_code_set)

_association = {'ASSOCIATED_WITH_LUN': 0x00,
                'ASSOCIATED_WITH_TARGET_PORT': 0x01,
                'ASSOCIATED_WITH_TARGET_DEVICE': 0x02, }

ASSOCIATION = Enum(_association)

_designator = {'VENDOR_SPECIFIC': 0x00,
               'T10_VENDOR_ID': 0x01,
               'EUI_64': 0x02,
               'NAA': 0x03,
               'RELATIVE_TARGET_PORT_IDENTIFIER': 0x04,
               'TARGET_PORTAL_GROUP': 0x05,
               'LOGICAL_UNIT_GROUP': 0x06,
               'MD5_LOGICAL_IDENTIFIER': 0x07,
               'SCSI_NAME_STRING': 0x08,
               'PCI_EXPRESS_ROUTING_ID': 0x09, }

DESIGNATOR = Enum(_designator)

_naa = {
    'IEEE_EXTENDED':                    0x02,
    'LOCALLY_ASSIGNED':                 0x03,
    'IEEE_REGISTERED':                  0x05,
    'IEEE_REGISTERED_EXTENDED':         0x06,
}

NAA = Enum(_naa)

#
# VPD pages
#

_vpds = {'SUPPORTED_VPD_PAGES': 0x00,
         'UNIT_SERIAL_NUMBER': 0x80,
         'DEVICE_IDENTIFICATION': 0x83,
         'SOFTWARE_INTERFACE_IDENTIFICATION': 0x84,
         'MANAGEMENT_NETWORK_ADDRESS': 0x85,
         'EXTENDED_INQUIRY_DATA': 0x86,
         'MODE_PAGE_POLICT': 0x87,
         'SCSI_PORTS': 0x88,
         'ATA_INFORMATION': 0x89,
         'POWER_CONDITION': 0x8a,
         'DEVICE_CONSTITUENTS': 0x8b,
         'CFA_PROFILE_INFORMATION': 0x8c,
         'POWER_CONSUMPTION': 0x8d,
         'THIRD_PARTY_COPY': 0x8f,
         'PROTOCOL_SPECIFIC_LOGICAL_UNIT_INFORMATION': 0x90,
         'PROTOCOL_SPECIFIC_PORT_INFORMATION': 0x91,
         #
         # SBC
         #
         'BLOCK_LIMITS': 0xb0,
         'BLOCK_DEVICE_CHARACTERISTICS': 0xb1,
         'LOGICAL_BLOCK_PROVISIONING': 0xb2,
         'REFERRALS': 0xb3,
         'SUPPORTED_BLOCK_LENGTHS_AND_PROTECTION_TYPES': 0xb4,
         'BLOCK_DEVICE_CHARACTERISTICS_EXTENSION': 0xb5, }

VPD = Enum(_vpds)
