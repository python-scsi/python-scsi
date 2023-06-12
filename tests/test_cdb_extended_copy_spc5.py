# coding: utf-8

# Copyright (C) 2023 by Brian Meagher <brian.meagher@ixsystems.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_extended_copy_spc5 import ExtendedCopy
from pyscsi.pyscsi.scsi_enum_command import spc
from pyscsi.pyscsi.scsi_enum_inquiry import ASSOCIATION, CODE_SET, DESIGNATOR, NAA
from pyscsi.utils.converter import scsi_ba_to_int
from tests.mock_device import MockDevice, MockSCSI


class CdbExtendedCopyTest(unittest.TestCase):
    def spstr(self, string_with_spaces):
        return string_with_spaces.replace(" ", "")

    def check_hex_str(self, hexstr, bytedict):
        count = int(len(hexstr) / 2)
        checkbytes = bytearray(count)
        for key in bytedict:
            checkbytes[key] = bytedict[key]
        self.assertEqual(hexstr, checkbytes.hex())

    def test_main(self):
        with MockSCSI(MockDevice(spc)) as s:
            r = s.extendedcopy5()
            self.assertIsInstance(r, ExtendedCopy)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.EXTENDED_COPY.value)
            self.assertEqual(
                cdb[1] & 0x1F,
                1,
            )
            self.assertEqual(cdb[2], 0x00)
            self.assertEqual(cdb[2:10], bytearray(8))
            self.assertEqual(scsi_ba_to_int(cdb[10:14]), 48)
            self.assertEqual(cdb[14], 0)
            self.assertEqual(len(cdb), 16)
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(cdb["opcode"], s.device.opcodes.EXTENDED_COPY.value)
            self.assertEqual(
                cdb["service_action"],
                1,
            )
            ExtendedCopy.unmarshall_cdb(ExtendedCopy.marshall_cdb(cdb))

            self.assertEqual(r.cdb.hex(), "83010000000000000000000000300000")
            self.assertEqual(len(r.dataout), 48)
            self.check_hex_str(r.dataout.hex(), {0: 1, 3: 0x20, 16: 0xFF})

            # STR
            r = s.extendedcopy5(sequential_striped=1)
            self.check_hex_str(r.dataout.hex(), {0: 1, 1: 0x20, 3: 0x20, 16: 0xFF})

            # LIST ID USAGE
            r = s.extendedcopy5(list_id_usage=1)
            self.check_hex_str(r.dataout.hex(), {0: 1, 1: 0x08, 3: 0x20, 16: 0xFF})
            r = s.extendedcopy5(list_id_usage=2)
            self.check_hex_str(r.dataout.hex(), {0: 1, 1: 0x10, 3: 0x20, 16: 0xFF})
            r = s.extendedcopy5(list_id_usage=3)
            self.check_hex_str(r.dataout.hex(), {0: 1, 1: 0x18, 3: 0x20, 16: 0xFF})

            # PRIORITY
            r = s.extendedcopy5(priority=1)
            self.check_hex_str(r.dataout.hex(), {0: 1, 1: 0x01, 3: 0x20, 16: 0xFF})
            r = s.extendedcopy5(priority=7)
            self.check_hex_str(r.dataout.hex(), {0: 1, 1: 0x07, 3: 0x20, 16: 0xFF})

            r = s.extendedcopy5(sequential_striped=1, list_id_usage=2, priority=5)
            self.check_hex_str(r.dataout.hex(), {0: 1, 1: 0x35, 3: 0x20, 16: 0xFF})

            # G_SENSE
            r = s.extendedcopy5(g_sense=1)
            self.check_hex_str(r.dataout.hex(), {0: 1, 3: 0x20, 15: 0x02, 16: 0xFF})

            # IMMED
            r = s.extendedcopy5(immed=1)
            self.check_hex_str(r.dataout.hex(), {0: 1, 3: 0x20, 15: 0x01, 16: 0xFF})

            # LIST IDENTIFIER
            r = s.extendedcopy5(list_identifier=255)
            self.check_hex_str(r.dataout.hex(), {0: 1, 3: 0x20, 23: 0xFF, 16: 0xFF})
            r = s.extendedcopy5(list_identifier=256)
            self.check_hex_str(r.dataout.hex(), {0: 1, 3: 0x20, 22: 0x01, 16: 0xFF})
            r = s.extendedcopy5(list_identifier=257)
            self.check_hex_str(
                r.dataout.hex(), {0: 1, 3: 0x20, 22: 0x01, 23: 0x01, 16: 0xFF}
            )

            # INLINE DATA
            r = s.extendedcopy5(inline_data=bytearray.fromhex("deadbeef"))
            self.assertEqual(len(r.dataout), 52)
            self.assertEqual(scsi_ba_to_int(r.cdb[10:14]), 52)
            self.check_hex_str(
                r.dataout.hex(),
                {
                    0: 1,
                    3: 0x20,
                    16: 0xFF,
                    47: 4,
                    48: 0xDE,
                    49: 0xAD,
                    50: 0xBE,
                    51: 0xEF,
                },
            )

            # CSCD
            r = s.extendedcopy5(
                cscd_descriptor_list=[
                    {
                        "descriptor_type_code": "Identification Descriptor CSCD descriptor",
                        "peripheral_device_type": 0x00,
                        "relative_initiator_port_identifier": 42,
                        "cscd_descriptor_parameters": {
                            "designator_type": DESIGNATOR.VENDOR_SPECIFIC,
                            "designator": {
                                "vendor_specific": bytearray.fromhex("deadbeef")
                            },
                        },
                        "device_type_specific_parameters": {
                            "pad": 1,
                        },
                    }
                ]
            )
            # EXTENDED COPY parameter list: 48 bytes
            # One CSCD descriptor:          32 bytes (for this descriptor_type_code)
            # Total bytes                   80
            self.assertEqual(len(r.dataout), 80)
            self.assertEqual(scsi_ba_to_int(r.cdb[10:14]), 80)
            self.check_hex_str(
                r.dataout.hex(),
                {
                    0: 1,
                    3: 0x20,
                    16: 0xFF,
                    43: 32,
                    48: 0xE4,  # Identification Descriptor CSCD descriptor
                    49: 0x00,  # Peripheral Device Type
                    51: 42,  # relative_initiator_port_identifier
                    55: 4,  # designator length
                    56: 0xDE,
                    57: 0xAD,
                    58: 0xBE,
                    59: 0xEF,
                    76: 4,  # pad
                },
            )

            r = s.extendedcopy5(
                cscd_descriptor_list=[
                    {
                        "descriptor_type_code": "Identification Descriptor CSCD descriptor",
                        "peripheral_device_type": 0x05,
                        "cscd_descriptor_parameters": {
                            "association": ASSOCIATION.ASSOCIATED_WITH_LUN,
                            "code_set": CODE_SET.BINARY,
                            "designator_type": DESIGNATOR.NAA,
                            "designator": {
                                "naa": NAA.IEEE_REGISTERED_EXTENDED,
                                "ieee_company_id": 0x589CFC,
                                "vendor_specific_identifier": 0x00000C44,
                                "vendor_specific_identifier_extension": 0xC482CC288FBC0D75,
                            },
                        },
                        "device_type_specific_parameters": {
                            "disk_block_length": 512,
                        },
                    }
                ]
            )
            self.assertEqual(len(r.dataout), 80)
            self.assertEqual(scsi_ba_to_int(r.cdb[10:14]), 80)
            self.check_hex_str(
                r.dataout.hex(),
                {
                    0: 1,
                    3: 0x20,
                    16: 0xFF,
                    43: 32,  # CSCD DESCRIPTOR LIST LENGTH (LSB)
                    48: 0xE4,  # Identification Descriptor CSCD descriptor
                    48 + 1: 0x05,  # Peripheral Device Type
                    48 + 4: 0x01,  # CODE_SET.BINARY: 0x01
                    # ASSOCIATION.ASSOCIATED_WITH_LUN: 0x00, DESIGNATOR.NAA: 0x03
                    48 + 5: 0x03,
                    # See 7.7.6.6.5 NAA IEEE Registered Extended designator format: 16 bytes
                    48 + 7: 0x10,
                    # NAA: 58 9C FC | 00 00 0C 44 | C4 82 CC 28 8F BC 0D 75
                    # NAA:  5 89 CF C|0 00 00 0C 44 | C4 82 CC 28 8F BC 0D 75
                    # NAA.IEEE_REGISTERED_EXTENDED: 6, first nibble of ieee_company_id: 5
                    48 + 8: 0x65,
                    48 + 9: 0x89,
                    48 + 10: 0xCF,
                    48 + 11: 0xC0,
                    48 + 12: 0x00,
                    48 + 13: 0x00,
                    48 + 14: 0x0C,
                    48 + 15: 0x44,
                    48 + 16: 0xC4,
                    48 + 17: 0x82,
                    48 + 18: 0xCC,
                    48 + 19: 0x28,
                    48 + 20: 0x8F,
                    48 + 21: 0xBC,
                    48 + 22: 0x0D,
                    48 + 23: 0x75,
                    78: 2,  # disk block length (512 == 0x200)
                },
            )

            r = s.extendedcopy5(
                cscd_descriptor_list=[
                    {
                        "descriptor_type_code": "Identification Descriptor CSCD descriptor",
                        "peripheral_device_type": "Stream or Tape",
                        "cscd_descriptor_parameters": {
                            "association": ASSOCIATION.ASSOCIATED_WITH_LUN,
                            "code_set": CODE_SET.ASCII,
                            "designator_type": DESIGNATOR.T10_VENDOR_ID,
                            "designator": {
                                "t10_vendor_id": "TrueNAS ".encode("ascii"),
                                "vendor_specific_id": "test123".encode("ascii"),
                            },
                        },
                        "device_type_specific_parameters": {
                            "pad": 1,
                            "fixed": 1,
                            "stream_block_length": 1024,
                        },
                    }
                ]
            )
            self.assertEqual(len(r.dataout), 80)
            self.assertEqual(scsi_ba_to_int(r.cdb[10:14]), 80)
            self.check_hex_str(
                r.dataout.hex(),
                {
                    0: 1,
                    3: 0x20,
                    16: 0xFF,
                    43: 32,
                    48: 0xE4,  # Identification Descriptor CSCD descriptor
                    48 + 1: 0x01,  # Peripheral Device Type
                    48 + 4: 0x02,  # CODE_SET.ASCII: 0x02
                    # ASSOCIATION.ASSOCIATED_WITH_LUN: 0x00, DESIGNATOR.T10_VENDOR_ID: 0x01
                    48 + 5: 0x01,
                    48 + 7: 0x0F,  # len("TrueNAS " + "test123") == 15
                    # See 7.7.6.4 T10 vendor ID based designator format
                    48 + 8: ord("T"),
                    48 + 9: ord("r"),
                    48 + 10: ord("u"),
                    48 + 11: ord("e"),
                    48 + 12: ord("N"),
                    48 + 13: ord("A"),
                    48 + 14: ord("S"),
                    48 + 15: ord(" "),
                    48 + 16: ord("t"),
                    48 + 17: ord("e"),
                    48 + 18: ord("s"),
                    48 + 19: ord("t"),
                    48 + 20: ord("1"),
                    48 + 21: ord("2"),
                    48 + 22: ord("3"),
                    48 + 28: 5,  # pad & fixed, see 6.6.5.4
                    48 + 30: 4,  # stream block length (1024 == 0x400)
                },
            )

            # INLINE DATA
            r = s.extendedcopy5(
                segment_descriptor_list=[
                    {
                        "descriptor_type_code": "Copy from block device to block device",
                        "dc": 1,
                        "source_cscd_descriptor_id": 1,
                        "destination_cscd_descriptor_id": 2,
                        "block_device_number_of_blocks": 1024,
                        "source_block_device_logical_block_address": 2048,
                        "destination_block_device_logical_block_address": 4096,
                    }
                ],
                inline_data=bytearray.fromhex("deadbeef"),
            )
            # length 48 + 28 + 4
            self.assertEqual(len(r.dataout), 80)
            self.assertEqual(scsi_ba_to_int(r.cdb[10:14]), 80)
            self.check_hex_str(
                r.dataout.hex(),
                {
                    0: 1,
                    3: 0x20,
                    16: 0xFF,
                    # SEGMENT DESCRIPTOR LIST LENGTH
                    45: 28,
                    # INLINE DATA LENGTH
                    47: 4,
                    # DESCRIPTOR TYPE CODE: 0x02
                    48 + 0: 0x02,
                    # DC: 1
                    48 + 1: 0x02,
                    # DESCRIPTOR LENGTH (LSB): 24
                    48 + 3: 0x18,
                    # SOURCE CSCD DESCRIPTOR ID (LSB): 1
                    48 + 5: 1,
                    # DESTINATION CSCD DESCRIPTOR ID (LSB): 2
                    48 + 7: 2,
                    # BLOCK DEVICE NUMBER OF BLOCKS (MSB) 0x04 (1024 == 0x400)
                    48 + 10: 0x04,
                    # SOURCE BLOCK DEVICE LOGICAL BLOCK ADDRESS: (2048 == 0x800)
                    48 + 18: 0x08,
                    # DESTINATION BLOCK DEVICE LOGICAL BLOCK: (4096 = 0x1000)
                    48 + 26: 0x10,
                    # INLINE DATA
                    48 + 28 + 0: 0xDE,
                    48 + 28 + 1: 0xAD,
                    48 + 28 + 2: 0xBE,
                    48 + 28 + 3: 0xEF,
                },
            )
