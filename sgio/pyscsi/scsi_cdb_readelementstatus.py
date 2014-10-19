# coding: utf-8

from scsi_command import SCSICommand, OPCODE
from sgio.utils.converter import scsi_int_to_ba, scsi_ba_to_int
from sgio.utils.enum import Enum

#
# SCSI ReadElementStatus command and definitions
#

#
# qqq
#
header_bits = {'ps': [0x80, 0],
               'spf': [0x40, 0],
               'page_code': [0x3f, 0],
               'parameter_list_length': [0xff, 1], }

#
# Element Type Code
#
element_type = {'ALL': 0x00,
                'MEDIUM_TRANSPORT': 0x01,
                'STORAGE': 0x02,
                'IMPORT_EXPORT': 0x03,
                'DATA_TRANSFER': 0x04, }

ELEMENT_TYPE = Enum(element_type)

class ReadElementStatus(SCSICommand):
    """
    A class to hold information from a readelementstatus command
    """

    def __init__(self, scsi, start, num, element_type=ELEMENT_TYPE.ALL,
                 voltag=0, curdata=0, dvcid=0, alloclen=16384):
        """
        initialize a new instance

        :param scsi: a SCSI instance
        :param start: first element to return
        :param num: number of elements to return
        :param element_type: type of element to return data for
        :param voltag
        :param curdata
        :param dvcid
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self, scsi, 0, alloclen)
        self.cdb = self.build_cdb(start, num, element_type, voltag, curdata,
                                  dvcid, alloclen)
        self.execute()

    def build_cdb(self, start, num, element_type,
                  voltag, curdata, dvcid, alloclen):
        """
        """
        cdb = SCSICommand.init_cdb(OPCODE.READ_ELEMENT_STATUS)
        if voltag:
            cdb[1] |= 0x10
        cdb[1] |= element_type & 0x0f
        cdb[2:4] = scsi_int_to_ba(start, 2);
        cdb[4:6] = scsi_int_to_ba(num, 2);
        if curdata:
            cdb[6] |= 0x02
        if dvcid:
            cdb[6] |= 0x01
        cdb[7:10] = scsi_int_to_ba(alloclen, 3);
        return cdb

    def unmarshall(self):
        """
        """
        self.decode_bits(self.datain, header_bits)
