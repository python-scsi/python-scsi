#!/usr/bin/env python
# coding: utf-8
from pyscsi.pyscsi.scsi_enum_command import smc
from pyscsi.utils.converter import scsi_ba_to_int
from mock_device import MockDevice, MockSCSI
from pyscsi.pyscsi.scsi_cdb_openclose_exportimport_element import OpenCloseImportExportElement


def main():
    with MockSCSI(MockDevice(smc)) as s:
        m = s.opencloseimportexportelement(32, s.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT.serviceaction.CLOSE_IMPORTEXPORT_ELEMENT)
        cdb = m.cdb
        assert cdb[0] == s.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT.value
        assert scsi_ba_to_int(cdb[2:4]) == 32
        assert cdb[4] == 0x01
        cdb = m.unmarshall_cdb(cdb)
        assert cdb['opcode'] == s.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT.value
        assert cdb['element_address'] == 32
        assert cdb['action_code'] == s.device.opcodes.OPEN_CLOSE_IMPORT_EXPORT_ELEMENT.serviceaction.CLOSE_IMPORTEXPORT_ELEMENT

        d = OpenCloseImportExportElement.unmarshall_cdb(OpenCloseImportExportElement.marshall_cdb(cdb))
        assert d == cdb


if __name__ == "__main__":
    main()
