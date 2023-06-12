# coding: utf-8

# Copyright (C) 2023 by Brian Meagher <brian.meagher@ixsystems.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest

from pyscsi.pyscsi.scsi_cdb_extended_copy_spc4 import ExtendedCopy
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
            r = s.extendedcopy4()
            self.assertIsInstance(r, ExtendedCopy)
            cdb = r.cdb
            self.assertEqual(cdb[0], s.device.opcodes.EXTENDED_COPY.value)
            self.assertEqual(
                cdb[1] & 0x1F,
                0,
            )
            self.assertEqual(cdb[2], 0x00)
            self.assertEqual(cdb[2:10], bytearray(8))
            self.assertEqual(scsi_ba_to_int(cdb[10:14]), 16)
            self.assertEqual(cdb[14], 0)
            self.assertEqual(len(cdb), 16)
            cdb = r.unmarshall_cdb(cdb)
            self.assertEqual(cdb["opcode"], s.device.opcodes.EXTENDED_COPY.value)
            self.assertEqual(
                cdb["service_action"],
                0,
            )
            ExtendedCopy.unmarshall_cdb(ExtendedCopy.marshall_cdb(cdb))

            self.assertEqual(r.cdb.hex(), "83000000000000000000000000100000")
            self.assertEqual(len(r.dataout), 16)
            self.check_hex_str(r.dataout.hex(), {})

            # LIST IDENTIFIER
            r = s.extendedcopy4(list_identifier=0x50)
            self.check_hex_str(r.dataout.hex(), {0: 0x50})

            # STR
            r = s.extendedcopy4(sequential_striped=1)
            self.check_hex_str(r.dataout.hex(), {1: 0x20})

            # NRCR
            r = s.extendedcopy4(nrcr=1)
            self.check_hex_str(r.dataout.hex(), {1: 0x10})

            # PRIORITY
            r = s.extendedcopy4(priority=1)
            self.check_hex_str(r.dataout.hex(), {1: 0x01})

            r = s.extendedcopy4(sequential_striped=1, nrcr=1, priority=7)
            self.check_hex_str(r.dataout.hex(), {1: 0x37})

            r = s.extendedcopy4(list_identifier=9, sequential_striped=1, priority=5)
            self.check_hex_str(r.dataout.hex(), {0: 9, 1: 0x25})

            # INLINE DATA
            r = s.extendedcopy4(inline_data=bytearray.fromhex("deadbeef"))
            self.assertEqual(len(r.dataout), 20)
            self.assertEqual(scsi_ba_to_int(r.cdb[10:14]), 20)
            self.check_hex_str(
                r.dataout.hex(),
                {
                    15: 4,
                    16: 0xDE,
                    17: 0xAD,
                    18: 0xBE,
                    19: 0xEF,
                },
            )

            # target
            r = s.extendedcopy4(
                target_descriptor_list=[
                    {
                        "descriptor_type_code": "Identification descriptor target descriptor",
                        "peripheral_device_type": 0x00,
                        "relative_initiator_port_identifier": 42,
                        "target_descriptor_parameters": {
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
            # EXTENDED COPY parameter list: 16 bytes
            # One target descriptor:        32 bytes (for this descriptor_type_code)
            # Total bytes                   48
            self.assertEqual(len(r.dataout), 48)
            self.assertEqual(scsi_ba_to_int(r.cdb[10:14]), 48)
            self.check_hex_str(
                r.dataout.hex(),
                {
                    3: 0x20,
                    16 + 0: 0xE4,  # Identification Descriptor target descriptor
                    16 + 1: 0x00,  # Peripheral Device Type
                    16 + 3: 42,  # relative_initiator_port_identifier
                    16 + 7: 4,  # designator length
                    16 + 8: 0xDE,
                    16 + 9: 0xAD,
                    16 + 10: 0xBE,
                    16 + 11: 0xEF,
                    16 + 28 + 0: 4,  # pad
                },
            )

            r = s.extendedcopy4(
                list_identifier=0xAA,
                target_descriptor_list=[
                    {
                        "descriptor_type_code": "Identification descriptor target descriptor",
                        "peripheral_device_type": 0x05,
                        "target_descriptor_parameters": {
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
                ],
            )

            self.assertEqual(len(r.dataout), 48)
            self.assertEqual(scsi_ba_to_int(r.cdb[10:14]), 48)
            self.check_hex_str(
                r.dataout.hex(),
                {
                    # LIST IDENTIFIER
                    0: 0xAA,
                    # TARGET DESCRIPTOR LIST LENGTH (LSB)
                    3: 0x20,
                    16 + 0: 0xE4,  # Identification Descriptor target descriptor
                    16 + 1: 0x05,  # Peripheral Device Type
                    16 + 4: 0x01,  # CODE_SET.BINARY: 0x01
                    # ASSOCIATION.ASSOCIATED_WITH_LUN: 0x00, DESIGNATOR.NAA: 0x03
                    16 + 5: 0x03,
                    # See 7.7.6.6.5 NAA IEEE Registered Extended designator format: 16 bytes
                    16 + 7: 0x10,
                    # NAA: 58 9C FC | 00 00 0C 44 | C4 82 CC 28 8F BC 0D 75
                    # NAA:  5 89 CF C|0 00 00 0C 44 | C4 82 CC 28 8F BC 0D 75
                    # NAA.IEEE_REGISTERED_EXTENDED: 6, first nibble of ieee_company_id: 5
                    16 + 8: 0x65,
                    16 + 9: 0x89,
                    16 + 10: 0xCF,
                    16 + 11: 0xC0,
                    16 + 12: 0x00,
                    16 + 13: 0x00,
                    16 + 14: 0x0C,
                    16 + 15: 0x44,
                    16 + 16: 0xC4,
                    16 + 17: 0x82,
                    16 + 18: 0xCC,
                    16 + 19: 0x28,
                    16 + 20: 0x8F,
                    16 + 21: 0xBC,
                    16 + 22: 0x0D,
                    16 + 23: 0x75,
                    16 + 30: 2,  # disk block length (512 == 0x200) SPC-4 6.3.6.5
                },
            )

            r = s.extendedcopy4(
                target_descriptor_list=[
                    {
                        "descriptor_type_code": "Identification descriptor target descriptor",
                        "peripheral_device_type": "Stream or Tape",
                        "target_descriptor_parameters": {
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
            self.assertEqual(len(r.dataout), 48)
            self.assertEqual(scsi_ba_to_int(r.cdb[10:14]), 48)
            self.check_hex_str(
                r.dataout.hex(),
                {
                    # TARGET DESCRIPTOR LIST LENGTH (LSB)
                    3: 0x20,
                    16 + 0: 0xE4,  # Identification Descriptor target descriptor
                    16 + 1: 0x01,  # Peripheral Device Type
                    16 + 4: 0x02,  # CODE_SET.ASCII: 0x02
                    # ASSOCIATION.ASSOCIATED_WITH_LUN: 0x00, DESIGNATOR.T10_VENDOR_ID: 0x01
                    16 + 5: 0x01,
                    16 + 7: 0x0F,  # len("TrueNAS " + "test123") == 15
                    # See SPC-4 7.7.4.4 T10 vendor ID based designator format
                    16 + 8: ord("T"),
                    16 + 9: ord("r"),
                    16 + 10: ord("u"),
                    16 + 11: ord("e"),
                    16 + 12: ord("N"),
                    16 + 13: ord("A"),
                    16 + 14: ord("S"),
                    16 + 15: ord(" "),
                    16 + 16: ord("t"),
                    16 + 17: ord("e"),
                    16 + 18: ord("s"),
                    16 + 19: ord("t"),
                    16 + 20: ord("1"),
                    16 + 21: ord("2"),
                    16 + 22: ord("3"),
                    16 + 28: 5,  # pad & fixed, see SPC-4 6.3.6.6
                    16 + 30: 4,  # stream block length (1024 == 0x400)
                },
            )

            # INLINE DATA
            r = s.extendedcopy4(
                list_identifier=0x12,
                segment_descriptor_list=[
                    {
                        "descriptor_type_code": "Copy from block device to block device",
                        "dc": 1,
                        "source_target_descriptor_id": 1,
                        "destination_target_descriptor_id": 2,
                        "block_device_number_of_blocks": 1024,
                        "source_block_device_logical_block_address": 2048,
                        "destination_block_device_logical_block_address": 4096,
                    }
                ],
                inline_data=bytearray.fromhex("deadbeef"),
            )
            # length 16 + 28 + 4
            self.assertEqual(len(r.dataout), 48)
            self.assertEqual(scsi_ba_to_int(r.cdb[10:14]), 48)
            self.check_hex_str(
                r.dataout.hex(),
                {
                    # LIST IDENTIFIER
                    0: 0x12,
                    # SEGMENT DESCRIPTOR LIST LENGTH (LSB)
                    # SPC-4 6.3.7.5 Block device to block device operations => len 28
                    11: 28,
                    # INLINE DATA LENGTH (LSB)
                    15: 4,
                    # DESCRIPTOR TYPE CODE: 0x02
                    16 + 0: 0x02,
                    # DC: 1
                    16 + 1: 0x02,
                    # DESCRIPTOR LENGTH (LSB): 24
                    16 + 3: 0x18,
                    # SOURCE TARGET DESCRIPTOR ID (LSB): 1
                    16 + 5: 1,
                    # DESTINATION TARGET DESCRIPTOR ID (LSB): 2
                    16 + 7: 2,
                    # BLOCK DEVICE NUMBER OF BLOCKS (MSB) 0x04 (1024 == 0x400)
                    16 + 10: 0x04,
                    # SOURCE BLOCK DEVICE LOGICAL BLOCK ADDRESS: (2048 == 0x800)
                    16 + 18: 0x08,
                    # DESTINATION BLOCK DEVICE LOGICAL BLOCK: (4096 = 0x1000)
                    16 + 26: 0x10,
                    # INLINE DATA
                    16 + 28 + 0: 0xDE,
                    16 + 28 + 1: 0xAD,
                    16 + 28 + 2: 0xBE,
                    16 + 28 + 3: 0xEF,
                },
            )
