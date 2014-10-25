# coding: utf-8

from scsi_command import SCSICommand
from scsi_enum_command import OPCODE
from sgio.utils.converter import decode_bits
import scsi_enum_modesense6 as modesensense_enums

#
# SCSI ModeSense6 command and definitions
#


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
        cdb[2] |= page_code & 0x3f
        cdb[3] = sub_page_code
        cdb[4] = alloclen
        return cdb

    def unmarshall_cdb(self, cdb):
        """
        method to unmarshall a byte array containing a cdb.
        """
        _tmp = {}
        decode_bits(cdb, modesensense_enums.cdb_bits, _tmp)
        return _tmp

    def unmarshall(self):
        """
        """
        decode_bits(self.datain[0:4], modesensense_enums.mode_header_bits, self.result)
        _bdl = self.result['block_descriptor_length']

        block_descriptor = self.datain[4:]
        
        mode_data = block_descriptor[_bdl:]
        decode_bits(mode_data, modesensense_enums.page_header_bits, self.result)

        if self.page_code == modesensense_enums.PAGE_CODE.ELEMENT_ADDRESS_ASSIGNMENT:
            decode_bits(mode_data, modesensense_enums.element_address_assignment_bits,
                        self.result)
