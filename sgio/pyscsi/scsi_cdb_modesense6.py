# coding: utf-8

from scsi_command import SCSICommand, OPCODE
from sgio.utils.converter import scsi_int_to_ba, scsi_ba_to_int
from sgio.utils.enum import Enum

#
# SCSI ModeSense6 command and definitions
#

#
# Mode Header
#
mode_header_bits = {'mode_data_length': [0xff, 0],
                    'medium_type': [0xff, 1],
                    'device_specific_parameter': [0xff, 2],
                    'block_descriptor_length': [0xff, 3], }

#
# Page Header
#
page_header_bits = {'ps': [0x80, 0],
                    'spf': [0x40, 0],
                    'page_code': [0x3f, 0],
                    'parameter_list_length': [0xff, 1], }

#
# Page Control
#
pc = {'CURRENT': 0x00,
      'CHANGEABLE': 0x01,
      'DEFAULT': 0x02,
      'SAVED': 0x03, }

PC = Enum(pc)

#
# Page Codes
#

page_code = {
        #
        # SMC
        #
        'ELEMENT_ADDRESS_ASSIGNMENT':          0x1d,
}

PAGE_CODE = Enum(page_code)

class ModeSense6(SCSICommand):
    """
    A class to hold information from a moesense6 command
    """

    def __init__(self, scsi, page_code, sub_page_code=0, dbd=0, pc=0,
                 alloclen=96):
        """
        initialize a new instance

        :param scsi: a SCSI instance
        :param page_code: the page code for the vpd page
        :param sub_page_code:
        :param dbd:
        :param pc:
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self, scsi, 0, alloclen)
        self.page_code = page_code
        self.sub_page_code = sub_page_code
        self.cdb = self.build_cdb(self.page_code, self.sub_page_code, dbd, pc,
                                  alloclen)
        self.execute()

    def build_cdb(self, page_code, sub_page_code, dbd, pc, alloclen):
        """
        """
        cdb = SCSICommand.init_cdb(OPCODE.MODE_SENSE_6)
        if dbd:
            cdb[1] |= 0x08
        cdb[2] |= (pc << 6) & 0xc0
        cdb[2] |= page_code &0x3f
        cdb[3] = sub_page_code
        cdb[4] = alloclen
        return cdb

    def unmarshall(self):
        """
        """
        self.decode_bits(self.datain[0:4], mode_header_bits)
        bdl = self.result['block_descriptor_length']

        block_descriptor = self.datain[4:]
        
        mode_data = block_descriptor[bdl:]
        self.decode_bits(mode_data, page_header_bits)

        if self.page_code == PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT:
            self.add_result('first_medium_transport_element_address',
                            scsi_ba_to_int(mode_data[2:4]))
            self.add_result('num_medium_transport_elements',
                            scsi_ba_to_int(mode_data[4:6]))
            self.add_result('first_storage_element_address',
                            scsi_ba_to_int(mode_data[6:8]))
            self.add_result('num_storage_elements',
                            scsi_ba_to_int(mode_data[8:10]))
            self.add_result('first_import_element_address',
                            scsi_ba_to_int(mode_data[10:12]))
            self.add_result('num_import_elements',
                            scsi_ba_to_int(mode_data[12:14]))
            self.add_result('first_data_transfer_element_address',
                            scsi_ba_to_int(mode_data[14:16]))
            self.add_result('num_data_transfer_elements',
                            scsi_ba_to_int(mode_data[16:18]))
