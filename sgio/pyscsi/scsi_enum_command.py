# coding: utf-8

from sgio.utils.enum import Enum

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
           }

OPCODE = Enum(opcodes)

service_action_ins = {'READ_CAPACITY_16': 0x10, }

SERVICE_ACTION_IN = Enum(service_action_ins)

scsi_status = {'GOOD': 0x00,
               'CHECK_CONDITION': 0x02,
               'CONDITIONS_MET': 0x04,
               'BUSY': 0x08,
               'RESERVATION_CONFLICT': 0x18,
               'TASK_SET_FULL': 0x28,
               'ACA_ACTIVE': 0x30,
               'TASK_ABORTED': 0x40,
               'SGIO_ERROR': 0xff, }

SCSI_STATUS = Enum(scsi_status)
