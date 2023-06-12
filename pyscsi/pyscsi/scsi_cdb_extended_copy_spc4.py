# coding: utf-8

# Copyright (C) 2023 by Brian Meagher<brian.meagher@ixsystems.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

from pyscsi.pyscsi.scsi_cdb_inquiry import Inquiry
from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.utils.converter import encode_dict

#
# SCSI ReportTargetPortGroups command and definitions
#


class ExtendedCopy(SCSICommand):
    """
    A class to hold information from a SPC-4 ExtendedCopy command to a scsi device
    """

    # See SPC-4 6.3.1 EXTENDED COPY command introduction
    # Table 100 - EXTENDED COPY command
    _cdb_bits = {
        "opcode": [0xFF, 0],
        "service_action": [0x1F, 1],
        "parameter_list_length": [0xFFFFFFFF, 10],
    }

    # See SPC-4 6.3.1 EXTENDED COPY command introduction
    # Table 101 - EXTENDED COPY parameter list
    _parameter_list_bits = {
        "list_identifier": [0xFF, 0],
        "priority": [0x07, 1],
        "nrcr": [0x10, 1],
        "str": [0x20, 1],
        "target_descriptor_list_length": [0xFFFF, 2],
        "segment_descriptor_list_length": [0xFFFFFFFF, 8],
        "inline_data_length": [0xFFFFFFFF, 12],
    }

    # See SPC-4 6.3.6.1 Target descriptors introduction
    # Table 104 - Target descriptor format
    _target_descriptor_bits = {
        "descriptor_type_code": [0xFF, 0],
        "peripheral_device_type": [0x1F, 1],
        "lu_id_type": [0xC0, 1],
        "relative_initiator_port_identifier": [0xFFFF, 2],
    }

    # See SPC-4 6.3.6.5 Device type specific target descriptor parameters for block device types
    # Table 110 - Device type specific target descriptor parameters for block device types
    _device_specific_target_descriptor_parameters_block = {
        "pad": [0x04, 28],
        "disk_block_length": [0xFFFFFF, 29],
    }

    # See SPC-4 6.3.6.6 Device type specific target descriptor parameters for sequential-access device types
    # Table 111 - Device type specific target descriptor parameters for sequential-access device types
    _device_specific_target_descriptor_parameters_sequential = {
        "fixed": [0x01, 28],
        "pad": [0x04, 28],
        "stream_block_length": [0xFFFFFF, 29],
    }

    # See SPC-4 6.3.6.7 Device type specific target descriptor parameters for processor device types
    # Table 113 - Device type specific target descriptor parameters for processor device types
    _device_specific_target_descriptor_parameters_processor = {
        "pad": [0x04, 28],
    }

    # See SPC-4 6.3.6.1 Target descriptors introduction,
    # Table 103 - EXTENDED COPY target descriptor type codes
    _target_descriptor_type_codes = {
        0xE0: {"name": "Fibre Channel N_Port_Name target descriptor", "size": 32},
        0xE1: {"name": "Fibre Channel N_Port_ID target descriptor", "size": 32},
        0xE2: {
            "name": "Fibre Channel N_Port_ID With N_Port_Name Checking target descriptor",
            "size": 32,
        },
        0xE3: {"name": "Parallel Interface T_L target descriptor", "size": 32},
        0xE4: {"name": "Identification descriptor target descriptor", "size": 32},
        0xE5: {"name": "IPv4 target descriptor", "size": 32},
        0xE6: {"name": "Alias target descriptor", "size": 32},
        0xE7: {"name": "RDMA target descriptor", "size": 32},
        0xE8: {"name": "IEEE 1394 EUI-64 target descriptor", "size": 32},
        0xE9: {"name": "SAS Serial SCSI Protocol target descriptor", "size": 32},
        0xEA: {"name": "IPv6 target descriptor", "size": 64},
    }

    # See SPC-4 6.3.6.3 Identification descriptor target descriptor format
    # Table 108 - Identification descriptor target descriptor format
    _target_designator_bits = {
        "code_set": [0x0F, 0],
        "association": [0x30, 1],
        "designator_type": [0x0F, 1],
        "designator_length": [0xFF, 3],
    }

    # See SPC-4 6.3.6.1 Target descriptors introduction
    # Table 106 - Device type specific parameters in target descriptors
    # Also SPC-4 6.4.2 Standard INQUIRY data
    # Table 136 - Peripheral device type
    _device_type_codes = {
        0x00: {
            "name": "Block",
            "description": "Direct access block device (e.g., magnetic disk)",
        },
        0x01: {
            "name": "Stream or Tape",
            "description": "Sequential access device (e.g., magnetic tape)",
        },
        0x03: {"name": "Stream", "description": "Processor device"},
        0x04: {
            "name": "Block",
            "description": "Write-once device (e.g., some optical disks)",
        },
        0x05: {"name": "Block", "description": "CD/DVD device"},
        0x07: {
            "name": "Block",
            "description": "Optical memory device (e.g., some optical disks)",
        },
        0x0E: {
            "name": "Block",
            "description": "Simplified direct access device (e.g., magnetic disk)",
        },
    }

    # See SPC-4 6.3.7.1 Segment descriptors introduction
    # Table 114 - EXTENDED COPY segment descriptor type codes
    _segment_descriptor_type_codes = {
        0x00: {
            "name": "block -> stream",
            "description": "Copy from block device to stream device",
        },
        0x01: {
            "name": "stream -> block",
            "description": "Copy from stream device to block device",
        },
        0x02: {
            "name": "block -> block",
            "description": "Copy from block device to block device",
        },
        0x03: {
            "name": "stream -> stream",
            "description": "Copy from stream device to stream device",
        },
        0x04: {
            "name": "inline -> stream",
            "description": "Copy inline data to stream device",
        },
        0x05: {
            "name": "embedded -> stream",
            "description": "Copy embedded data to stream device",
        },
        0x06: {
            "name": "stream -> discard",
            "description": "Read from stream device and discard",
        },
        0x07: {
            "name": "Verify",
            "description": "Verify block or stream device operation",
        },
        0x08: {
            "name": "block<o> -> stream",
            "description": "Copy block device with offset to stream device",
        },
        0x09: {
            "name": "stream -> block<o>",
            "description": "Copy stream device to block device with offset",
        },
        0x0A: {
            "name": "block<o> -> block<o>",
            "description": "Copy block device with offset to block device with offset",
        },
        0x0B: {
            "name": "block -> stream&application client",
            "description": "Copy from block device to stream device and hold a copy of processed data for the application client",
        },
        0x0C: {
            "name": "stream -> block&application client",
            "description": "Copy from stream device to block device and hold a copy of processed data for the application client",
        },
        0x0D: {
            "name": "block -> block&application client",
            "description": "Copy from block device to block device and hold a copy of processed data for the application client",
        },
        0x0E: {
            "name": "stream -> stream&application client",
            "description": "Copy from stream device to stream device and hold a copy of processed data for the application client",
        },
        0x0F: {
            "name": "stream -> discard&application client",
            "description": "Read from stream device and hold a copy of processed data for the application client",
        },
        0x10: {
            "name": "filemark -> tape",
            "description": "Write filemarks to sequential access device",
        },
        0x11: {
            "name": "space -> tape",
            "description": "Space records or filemarks on sequential access device",
        },
        0x12: {
            "name": "locate -> tape",
            "description": "Locate on sequential access device",
        },
        0x13: {"name": "<i>tape -> <i>tape", "description": "Tape device image copy"},
        0x14: {
            "name": "Register persistent reservation key",
            "description": "Register persistent reservation key",
        },
        0x15: {
            "name": "Third party persistent reservations source I_T nexus",
            "description": "Third party persistent reservations source I_T nexus",
        },
    }

    # See SPC-4 6.3.7.3 Block device to stream device operations
    # Table 118 - Block device to or from stream device segment descriptor
    _segment_descriptor_bits_block_to_stream = {
        "descriptor_type_code": [0xFF, 0],
        "cat": [0x01, 1],
        "descriptor_length": [0xFFFF, 2],
        "source_target_descriptor_id": [0xFFFF, 4],
        "destination_target_descriptor_id": [0xFFFF, 6],
        "stream_device_transfer_length": [0xFFFFFF, 9],
        "block_device_number_of_blocks": [0xFFFF, 14],
        "block_device_logical_block_address": [0xFFFFFFFFFFFFFFFF, 16],
    }

    # See SPC-4 6.3.7.4 Stream device to block device operations
    _segment_descriptor_bits_stream_to_block = _segment_descriptor_bits_block_to_stream

    # See SPC-4 6.3.7.5 Block device to block device operations
    # Table 119 - Block device to block device segment descriptor
    _segment_descriptor_bits_block_to_block = {
        "descriptor_type_code": [0xFF, 0],
        "cat": [0x01, 1],
        "dc": [0x02, 1],
        "descriptor_length": [0xFFFF, 2],
        "source_target_descriptor_id": [0xFFFF, 4],
        "destination_target_descriptor_id": [0xFFFF, 6],
        "block_device_number_of_blocks": [0xFFFF, 10],
        "source_block_device_logical_block_address": [0xFFFFFFFFFFFFFFFF, 12],
        "destination_block_device_logical_block_address": [0xFFFFFFFFFFFFFFFF, 20],
    }

    def __init__(
        self,
        opcode,
        list_identifier=0,
        sequential_striped=0,
        nrcr=0,
        priority=0,
        target_descriptor_list=[],
        segment_descriptor_list=[],
        inline_data=bytearray(0),
    ):
        """
        initialize a new instance

        :param opcode: a OpCode instance

        :param list_identifier Identifies the copy operation.  See SPC-4
        6.3.1 EXTENDED COPY command introduction

        :param sequential_striped: A sequential striped (STR) bit set to one
        specifies to the copy manager that the majority of the block device
        references in the parameter list represent sequential access of several
        block devices that are striped.  A STR bit set to zero specifies to the
        copy manager that disk references, if any, may not be sequential.

        :param nrcr: No Receive Copy Results.  See SPC-4 6.3.1 EXTENDED COPY command introduction

        :param priority: specifies the priority of data transfers resulting from
        this EXTENDED COPY command relative to data transfers resulting from
        other commands being processed by the device server contained within the
        same logical unit as the copy manager.  All commands other than
        third-party copy commands have a priority of 1h. Priority 0h is the
        highest priority, with increasing values in the PRIORITY field
        indicating lower priorities.

        :param target_descriptor_list: list of target descriptors

        :param segment_descriptor_list: list of segment descriptors.  See
        SPC-4 6.3.7 Segment descriptors.  Each descriptor is a dic

        :param inline_data: The inline data contains information that is
        available for reference by target descriptors; or transfer by the copy
        manager in response to segment descriptors.

        EXAMPLE USAGE:

        r = s1.extendedcopy4(
            priority=1,
            list_identifier=0x34,
            target_descriptor_list=[
                {
                    "descriptor_type_code": "Identification descriptor target descriptor",
                    "device_type_specific_parameters": {"disk_block_length": 512},
                    "peripheral_device_type": 0,
                    "target_descriptor_parameters": {
                        "association": 0,
                        "code_set": 1,
                        "designator": {
                            "ieee_company_id": 5807356,
                            "naa": 6,
                            "vendor_specific_identifier": 3140,
                            "vendor_specific_identifier_extension": 14160104652988484981,
                        },
                        "designator_length": 16,
                        "designator_type": 3,
                    },
                },
                {
                    "descriptor_type_code": "Identification descriptor target descriptor",
                    "device_type_specific_parameters": {"disk_block_length": 512},
                    "peripheral_device_type": 0,
                    "target_descriptor_parameters": {
                        "association": 0,
                        "code_set": 1,
                        "designator": {
                            "ieee_company_id": 5807356,
                            "naa": 6,
                            "vendor_specific_identifier": 3809,
                            "vendor_specific_identifier_extension": 17655255278882869693,
                        },
                        "designator_length": 16,
                        "designator_type": 3,
                    },
                },
            ],
            segment_descriptor_list=[
                {
                    "block_device_number_of_blocks": 4,
                    "dc": 1,
                    "descriptor_type_code": "Copy from block device to block device",
                    "destination_block_device_logical_block_address": 10,
                    "destination_target_descriptor_id": 1,
                    "source_block_device_logical_block_address": 1,
                    "source_target_descriptor_id": 0,
                }
            ],
        )

        """
        SCSICommand.__init__(self, opcode, 0, 0)

        # payload
        self.dataout = self.marshall_parameter_list(
            list_identifier,
            sequential_striped,
            nrcr,
            priority,
            target_descriptor_list,
            segment_descriptor_list,
            inline_data,
        )

        # This is SPC-4 which has a service_action of 0, different than SPC-5
        self.cdb = self.build_cdb(
            opcode=self.opcode.value,
            parameter_list_length=len(self.dataout),
        )

    @classmethod
    def marshall_parameter_list(
        cls,
        list_identifier,
        sequential_striped,
        nrcr,
        priority,
        target_descriptor_list,
        segment_descriptor_list,
        inline_data,
    ):
        target_data = []
        for target_dict in target_descriptor_list:
            target_data.append(cls.marshall_target(target_dict))
        target_descriptor_list_length = sum([len(item) for item in target_data])

        segment_data = []
        for segment_dict in segment_descriptor_list:
            segment = cls.marshall_segment(segment_dict)
            if segment:
                segment_data.append(segment)
            else:
                raise ValueError("Failed to generate segment for %s" % segment_dict)
        segment_descriptor_list_length = sum([len(item) for item in segment_data])

        inline_data_length = len(inline_data)

        # Write the header.  See 6.6.2 EXTENDED COPY parameter data,
        # Table 99 — EXTENDED COPY parameter list
        _r = bytearray(16)
        _data = {
            "list_identifier": list_identifier,
            "priority": priority,
            "nrcr": nrcr,
            "str": sequential_striped,
            "header_target_descriptor_list_length": 0x20,
            "target_descriptor_list_length": target_descriptor_list_length,
            "segment_descriptor_list_length": segment_descriptor_list_length,
            "inline_data_length": inline_data_length,
        }
        encode_dict(_data, cls._parameter_list_bits, _r)

        return _r + b"".join(target_data) + b"".join(segment_data) + inline_data

    @classmethod
    def marshall_target(cls, target_dict):
        """
        Marshall a target descriptor

        :param target_dict: a dict with keys

          descriptor_type_code:

          peripheral_device_type:

          lu_id_type:

          relative_initiator_port_identifier:

          param target_descriptor_parameters: Dictionary with parameters based on
          the value of descriptor_type_code

              descriptor_type_code == 0xE4, See SPC-4 6.6.5.6 Identification
              Descriptor target descriptor format.  Keys:

                code_set
                designator_type
                association
                designator_length
                designator

          device_type_specific_parameters: A dict with keys that vary based on
          peripheral_device_type.

          For block, sequential or processor device types:
            pad: The PAD bit is used in conjunction with the CAT bit in the
            segment descriptor to determine what action should be taken if a
            segment of the copy does not fit exactly into an integer number of
            destination logical blocks

          For block device type:
            disk_block_length: If the DISK BLOCK LENGTH field is set to zero
            and the PERIPHERAL DEVICE TYPE field is set to 00h, then the copy
            manager shall determine the logical block length of the target
            logical unit (e.g., by sending a READ CAPACITY command, and use
            the result wherever the use of the DISK BLOCK LENGTH field is
            required by this standard.

          For the sequential access device type:
            fixed: FIXED bit

            stream_block_length: The contents of the FIXED bit and STREAM BLOCK
            LENGTH field are combined with the STREAM DEVICE TRANSFER LENGTH
            FIELD in the segment descriptor to determine the length of the
            stream read or write operation as specified in SPC-4 6.3.6.6 Device
            type specific target descriptor parameters for sequential-access
            device types, Table 112 - Stream device transfer lengths

        :return result: a byte array
        """
        # First check the keys
        valid_keys = set(cls._target_descriptor_bits.keys()).union(
            [
                "target_descriptor_parameters",
                "device_type_specific_parameters",
            ]
        )
        provided_keys = set(target_dict.keys())
        if not provided_keys.issubset(valid_keys):
            for key in provided_keys:
                raise ValueError(
                    "Invalid key supplied: %s (should be one of %s)" % (key, valid_keys)
                )

        # Now check some values
        descriptor_type_code = cls.get_code_int(
            "descriptor_type_code", target_dict, cls._target_descriptor_type_codes
        )
        peripheral_device_type = cls.get_code_int(
            "peripheral_device_type", target_dict, cls._device_type_codes
        )

        lu_id_type = target_dict.get("lu_id_type", 0)
        if lu_id_type != 0:
            raise ValueError("Invalid lu_id_type provided: %d" % lu_id_type)

        relative_initiator_port_identifier = target_dict.get(
            "relative_initiator_port_identifier", 0
        )

        numbytes = cls._target_descriptor_type_codes[descriptor_type_code]["size"]
        _data = bytearray(numbytes)

        #
        # Write the header of the target descriptor
        #
        # See SPC-4 6.3.6.1 Target descriptors introduction
        # Table 104 - Target descriptor format
        encode_dict(
            {
                "descriptor_type_code": descriptor_type_code,
                "peripheral_device_type": peripheral_device_type,
                "lu_id_type": lu_id_type,
                "relative_initiator_port_identifier": relative_initiator_port_identifier,
            },
            cls._target_descriptor_bits,
            _data,
        )

        #
        # target descriptor parameters
        #
        cls.marshall_target_descriptor_parameters(
            descriptor_type_code,
            _data,
            target_dict.get("target_descriptor_parameters", {}),
        )

        #
        # Device type specific parameters
        #
        params = target_dict.get("device_type_specific_parameters", {})
        if peripheral_device_type in [0x00, 0x04, 0x05, 0x07, 0x0E]:
            encode_dict(
                {
                    "pad": params.get("pad", 0),
                    "disk_block_length": params.get("disk_block_length", 0),
                },
                cls._device_specific_target_descriptor_parameters_block,
                _data,
            )
        elif peripheral_device_type == 0x01:
            encode_dict(
                {
                    "fixed": params.get("fixed", 0),
                    "pad": params.get("pad", 0),
                    "stream_block_length": params.get("stream_block_length", 0),
                },
                cls._device_specific_target_descriptor_parameters_sequential,
                _data,
            )
        elif peripheral_device_type == 0x03:
            encode_dict(
                {
                    "pad": params.get("pad", 0),
                },
                cls._device_specific_target_descriptor_parameters_processor,
                _data,
            )

        return _data

    @classmethod
    def marshall_target_descriptor_parameters(
        cls, descriptor_type_code, data, target_descriptor_parameters
    ):
        """
        Marshall the target descriptor parameters for a target descriptor.

        :param descriptor_type_code: See SPC-4 6.3.6.1 Target descriptors introduction,
        Table 103 - EXTENDED COPY target descriptor type codes

        :param data: bytearray reppresenting the CSCD descriptor

        :param target_descriptor_parameters: Dictionary with parameters based on
        the value of descriptor_type_code

          descriptor_type_code == 0xE4, See SPC-4 6.6.5.6 Identification
          Descriptor CSCD descriptor format.  Keys:

            code_set
            designator_type
            association
            designator_length
            designator

        """
        if descriptor_type_code == 0xE0:
            # Fibre Channel N_Port_Name CSCD descriptor
            pass
        elif descriptor_type_code == 0xE1:
            # Fibre Channel N_Port_ID CSCD descriptor
            pass
        elif descriptor_type_code == 0xE2:
            # Fibre Channel N_Port_ID With N_Port_Name Checking CSCD descriptor
            pass
        elif descriptor_type_code == 0xE4:
            # Identification Descriptor CSCD descriptor
            #
            # The structure shown in SPC-4 6.3.6.3 Identification descriptor target
            # descriptor format, Table 108 — Identification Descriptor target
            # descriptor format matches the format shown in SPC-4 7.7.4.1 Device
            # Identification VPD page overview, Table 486 - Designation
            # descriptor ... albeit at a different byte offset (and without the
            # PROTOCOL IDENTIFIER or PIV fields)
            #
            # Therefore, we can reuse the Inquiry.marshall_designator class
            # method here.  We implement our own marshall_designator_descriptor
            # as we do NOT want the protocol_identifier and piv fields supported
            # by inquiry.
            designator = cls.marshall_designator_descriptor(
                target_descriptor_parameters
            )
            data[4 : 4 + len(designator)] = designator
            return
        elif descriptor_type_code == 0xE5:
            # IPv4 CSCD descriptor
            pass
        elif descriptor_type_code == 0xE6:
            # Alias CSCD descriptor
            pass
        elif descriptor_type_code == 0xE7:
            # RDMA CSCD descriptor
            pass
        elif descriptor_type_code == 0xE8:
            # IEEE 1394 EUI-64 CSCD descriptor
            pass
        elif descriptor_type_code == 0xE9:
            # SAS Serial SCSI Protocol CSCD descriptor
            pass
        elif descriptor_type_code == 0xEA:
            # IPv6 CSCD descriptor
            pass
        elif descriptor_type_code == 0xEB:
            # IP Copy Service CSCD descriptor
            pass
        elif descriptor_type_code == 0xEC:
            # Multiple Device CSCD descriptor"
            pass
        elif descriptor_type_code == 0xFE:
            # ROD CSCD descriptor
            pass
        else:
            raise ValueError("Invalid descriptor type code: %s" % descriptor_type_code)

        raise NotImplementedError(
            "CSCD descriptor parameter not yet implemented for %s (%s)"
            % (
                hex(descriptor_type_code),
                cls._target_descriptor_type_codes[descriptor_type_code]["name"],
            )
        )

    @classmethod
    def marshall_designator_descriptor(cls, data):
        """
        static helper method to marshall designator desciptor data

        :param data: a dict with designator data
        :return: a byte array
        """
        _r = bytearray(4)
        encode_dict(data, cls._target_designator_bits, _r)

        _r += Inquiry.marshall_designator(data["designator_type"], data["designator"])
        _r[3] = len(_r) - 4
        return _r

    @classmethod
    def marshall_segment(cls, segment_dict):
        """
        Marshall a segment descriptor

        :param segment_dict: a dict with keys

          descriptor_type_code:
          cat:
          dc:
          fco:
        """
        descriptor_type_code = cls.get_code_int(
            "descriptor_type_code", segment_dict, cls._segment_descriptor_type_codes
        )

        # Update the descriptor_type_code in case an int was not supplied
        segment_dict["descriptor_type_code"] = descriptor_type_code

        if descriptor_type_code in [0x00, 0x0B]:
            return cls.encode_segment_dict(
                segment_dict, cls._segment_descriptor_bits_block_to_stream, 24
            )
        elif descriptor_type_code in [0x01, 0x0C]:
            return cls.encode_segment_dict(
                segment_dict, cls._segment_descriptor_bits_stream_block, 24
            )
        elif descriptor_type_code in [0x02, 0x0D]:
            return cls.encode_segment_dict(
                segment_dict, cls._segment_descriptor_bits_block_to_block, 28
            )

        raise NotImplementedError(
            "segment descriptor parameter not yet implemented for %s (%s)"
            % (
                hex(descriptor_type_code),
                cls._segment_descriptor_type_codes[descriptor_type_code]["name"],
            )
        )

    @classmethod
    def encode_segment_dict(cls, data_dict, check_dict, numbytes):
        data_dict["descriptor_length"] = numbytes - 4

        valid_keys = set(check_dict.keys())
        provided_keys = set(data_dict.keys())
        if not provided_keys.issubset(valid_keys):
            for key in provided_keys:
                raise ValueError(
                    "Invalid key supplied: %s (should be one of %s)" % (key, valid_keys)
                )

        _r = bytearray(numbytes)
        encode_dict(data_dict, check_dict, _r)
        return _r

    @classmethod
    def get_code_int(cls, key, datadict, table):
        """
        Return the integer value associated with the supplied value.
        """
        value = datadict.get(key)
        if value is not None:
            # Is value is a key to the table (usual case)
            if value in table:
                return value

            # Is value is a name or description in the table
            for k, v in table.items():
                if value == v.get("name"):
                    return k
                if value == v.get("description"):
                    return k

        # Could not find value!
        raise ValueError("Invalid %s provided: %s" % (key, value))
