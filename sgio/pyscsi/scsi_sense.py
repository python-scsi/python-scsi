# coding: utf-8

#      Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
#
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU Lesser General Public License as published by
#	   the Free Software Foundation; either version 2.1 of the License, or
#	   (at your option) any later version.
#
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU Lesser General Public License for more details.
#
#	   You should have received a copy of the GNU Lesser General Public License
#	   along with this program; if not, see <http://www.gnu.org/licenses/>.

#
# SPC4 4.6 Sense Data
#
SENSE_FORMAT_CURRENT_FIXED       = 0x70
SENSE_FORMAT_DEFERRED_FIXED      = 0x71
SENSE_FORMAT_CURRENT_DESCRIPTOR  = 0x72
SENSE_FORMAT_DEFERRED_DESCRIPTOR = 0x73

# dict with common key code qualifiers
sense_key_dict = { 0x00: 'No Sense',
                   0x01: 'Recovered Error',
                   0x02: 'Not Ready',
                   0x03: 'Medium Error',
                   0x04: 'Hardware Error',
                   0x05: 'Illegal Request',
                   0x06: 'Unit Attention',
                   0x07: 'Data Protect',
                   0x08: 'Blank Check',
                   0x09: 'Vendor Specific',
                   0x0a: 'Copy Aborted',
                   0x0b: 'Aborted Command',
                   0x0d: 'Volume Overflow',
                   0x0e: 'Miscompare',
                   0x0f: 'Completed'}

# dict with additional sense data
sense_ascq_dict = { 0x2400: 'Invalid Field In CDB',
                    0x2401: 'CDB Decryption Error',
                    0x2404: 'Security Audit Value Frozen',
                    0x2405: 'Security Working Key Frozen',
                    0x2406: 'Nonce Not Unique',
                    0x2407: 'Nonce Timestamp Out Of Range',
                    0x2408: 'Invalid XCDB'
                    }

# Exception Class for a SCSI REQUEST SENSE command
class SCSICheckCondition(Exception):
    '''Exception raised for errors in the SCSIDevice execute method

    Attributes:
        sense -- bytearray with additional data
    '''
    def __init__(self, sense):
        self.valid = sense[0] & 0x80
        self.response_code = sense[0] & 0x7f

        print "Response code 0x%02x" % (self.response_code)
        if self.response_code == SENSE_FORMAT_CURRENT_FIXED:
            self.filemark = sense[2] & 0x80
            self.eom = sense[2] & 0x40
            self.ili = sense[2] & 0x20
            self.sdat_ovfl = sense[2] & 0x10
            self.sense_key = sense[2] & 0x0f
            self.information = sense[3:7]
            self.additional_sense_length = sense[7]
            self.command_specific_information = sense[8:12]
            self.additional_sense_code = sense[12]
            self.additional_sense_code_qualifier = sense[13]
            self.field_replaceable_unit_code = sense[14]

            self.ascq = self.additional_sense_code << 8 + self.additional_sense_code_qualifier

    def __str__(self):
        return "Check Condition: %s(0x%02x) ASC+Q:%s(0x%04x)" % (
            sense_key_dict[self.sense_key], self.sense_key,
            sense_ascq_dict[self.ascq], self.ascq)

