# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import pyscsi.pyscsi.scsi_enum_inquiry as inquiry_enums
import pyscsi.utils.converter as convert
from pyscsi.pyscsi.scsi_command import SCSICommand

#
# SCSI Inquiry command and definitions
#

# we get a generator for all inquiry enums, so we can add them to the class
_enums = ((key, inquiry_enums.__dict__[key]) for key in inquiry_enums.__dict__.keys()
          if key in inquiry_enums.__all__)


class Inquiry(SCSICommand):
    """
    A class to hold information from a inquiry command to a scsi device
    """
    _cdb_bits =                          {'opcode': [0xff, 0],
                                          'evpd': [0x01, 1],
                                          'page_code': [0xff, 2],
                                          'alloc_len': [0xffff, 3], }

    _datain_bits =                       {'peripheral_qualifier': [0xe0, 0],
                                          'peripheral_device_type': [0x1f, 0], }

    _standard_bits =                     {'rmb': [0x80, 1],
                                          'version': [0xff, 2],
                                          'normaca': [0x20, 3],
                                          'hisup': [0x10, 3],
                                          'response_data_format': [0x0f, 3],
                                          'additional_length': [0xff, 4],
                                          'sccs': [0x80, 5],
                                          'acc': [0x40, 5],
                                          'tpgs': [0x30, 5],
                                          '3pc': [0x08, 5],
                                          'protect': [0x01, 5],
                                          'encserv': [0x40, 6],
                                          'vs': [0x20, 6],
                                          'multip': [0x10, 6],
                                          'addr16': [0x01, 6],
                                          'wbus16': [0x20, 7],
                                          'sync': [0x10, 7],
                                          'cmdque': [0x02, 7],
                                          'vs2': [0x01, 7],
                                          't10_vendor_identification': ('b', 8, 8),
                                          'product_identification': ('b', 16, 16),
                                          'product_revision_level': ('b', 32, 4),
                                          'clocking': [0x0c, 56],
                                          'qas': [0x02, 56],
                                          'ius': [0x01, 56], }

    _pagecode_bits =                     {'page_code': [0xff, 1], }

    _block_limits_bits =                 {'wsnz': [0x01, 4],
                                          'ugavalid': [0x80, 32],
                                          'max_caw_len': [0xff, 5],
                                          'opt_xfer_len_gran': [0xffff, 6],
                                          'max_xfer_len': [0xffffffff, 8],
                                          'opt_xfer_len': [0xffffffff, 12],
                                          'max_pfetch_len': [0xffffffff, 16],
                                          'max_unmap_lba_count': [0xffffffff, 20],
                                          'max_unmap_bd_count': [0xffffffff, 24],
                                          'opt_unmap_gran': [0xffffffff, 28],
                                          'unmap_gran_alignment': [0xffffffff, 32],
                                          'max_ws_len': [0xffffffff, 36], }

    _block_dev_char_bits =               {'medium_rotation_rate': [0xffff, 4],
                                          'product_type': [0xff, 6],
                                          'wabereq': [0xc0, 7],
                                          'wacereq': [0x30, 7],
                                          'nominal_form_factor': [0x0f, 7],
                                          'fuab': [0x02, 8],
                                          'vbuls': [0x01, 8], }

    _logical_block_provisioning_bits =   {'threshold_exponent': [0xff, 4],
                                          'lbpu': [0x80, 5],
                                          'lpbws': [0x40, 5],
                                          'lbpws10': [0x20, 5],
                                          'lbprz': [0x04, 5],
                                          'anc_sup': [0x02, 5],
                                          'dp': [0x01, 5],
                                          'provisioning_type': [0x07, 6], }

    _referrals_bits =                    {'user_data_segment_size': [0xffffffff, 8],
                                          'user_data_segment_multiplier': [0xffffffff, 12], }
    _extended_bits =                     {'activate_microcode': [0xc0, 4],
                                          'spt': [0x38, 4],
                                          'grd_chk': [0x04, 4],
                                          'app_chk': [0x02, 4],
                                          'ref_chk': [0x01, 4],
                                          'uask_sup': [0x20, 5],
                                          'group_sup': [0x10, 5],
                                          'prior_sup': [0x08, 5],
                                          'headsup': [0x04, 5],
                                          'ordsup': [0x02, 5],
                                          'simpsup': [0x01, 5],
                                          'wu_sup': [0x08, 6],
                                          'crd_sup': [0x04, 6],
                                          'nv_sup': [0x02, 6],
                                          'v_sup': [0x01, 6],
                                          'p_i_i_sup': [0x10, 7],
                                          'luiclr': [0x01, 7],
                                          'r_sup': [0x10, 8],
                                          'cbcs': [0x01, 8],
                                          'multi_it_nexus_microcode_download': [0x0f, 9],
                                          'extended_self_test_completion_minutes': [0xffff, 10],
                                          'poa_sup': [0x80, 12],
                                          'hra_sup': [0x40, 12],
                                          'vsa_sup': [0x20, 12],
                                          'maximum_supported_sense_data_length': [0xff, 13], }

    _designator_bits =                   {'protocol_identifier': [0xf0, 0],
                                          'code_set': [0x0f, 0],
                                          'piv': [0x80, 1],
                                          'association': [0x30, 1],
                                          'designator_type': [0x0f, 1],
                                          'designator_length': [0xff, 3], }

    _naa_type_bits =                     {'naa': [0xf0, 0], }

    _naa_ieee_extended_bits =            {'vendor_specific_identifier_a': [0x0fff, 0],
                                          'ieee_company_id': [0xffffff, 2],
                                          'vendor_specific_identifier_b': [0xffffff, 5], }

    _naa_locally_assigned_bits =         {'locally_administered_value': [0x0fffffffffffffff, 0], }
    _naa_ieee_registered_bits =          {'ieee_company_id': [0x0ffffff0, 0],
                                          'vendor_specific_identifier': [0x0fffffffff, 3], }

    _naa_ieee_registered_extended_bits = {'ieee_company_id': [0x0ffffff0, 0],
                                          'vendor_specific_identifier': [0x0fffffffff, 3],
                                          'vendor_specific_identifier_extension': [0xffffffffffffffff, 8], }
    _relative_port_bits =                {'relative_port': [0xffff, 2], }

    _target_portal_group_bits =          {'target_portal_group': [0xffff, 2], }

    _logical_unit_group_bits =           {'logical_unit_group': [0xffff, 2], }

    _pci_express_routing_id_bits =       {'pci_express_routing_id': [0xffff, 0], }

    _ata_information_bits =              {'sat_vendor_identification': ('b', 8, 8),
                                          'sat_product_identification': ('b', 16, 20),
                                          'sat_product_rev_lvl': ('b', 32, 4), }

    _ata_signature_bits =                {'sector_count': [0xff, 0],
                                          'lba_low': [0xff, 1],
                                          'lba_mid': [0xff, 2],
                                          'lba_high': [0xff, 3],
                                          'device': [0xff, 4], }

    _ata_identify_bits =                 {'general_config': [0xffffffff, 0],
                                          'specific_config': [0xffffffff, 4],
                                          'serial_number': ('w', 10, 10),
                                          'firmware_rev': ('w', 23, 4),
                                          'model_number': ('w', 27, 20), }

    _ata_identify_gen_conf_bits =        {'ata_device': [0x80, 1],
                                          'respose_incomplete': [0x02, 0], }

    # HACK: we update the baseclass with enums for the subclass, if there is a better way
    #       to add this to the subclass we should use it instead :-)
    for enum in _enums:
        setattr(SCSICommand, enum[0], enum[1])

    def __init__(self,
                 opcode,
                 evpd=0,
                 page_code=0,
                 alloclen=96):
        """
        initialize a new instance

        :param opcode: a OpCode instance
        :param evpd: the byte to enable or disable vital product data
        :param page_code: the page code for the vpd page
        :param alloclen: the max number of bytes allocated for the data_in buffer
        """
        SCSICommand.__init__(self,
                             opcode,
                             0,
                             alloclen)
        self._evpd = evpd
        self.cdb = self.build_cdb(opcode=self.opcode.value,
                                  evpd=evpd,
                                  page_code=page_code,
                                  alloc_len=alloclen)

    @classmethod
    def marshall_designator(cls,
                            _type,
                            data):
        """
        static helper method to marshall designator data

        :param _type: type of the designator
        :param data: a dict with designator data
        :return: a byte array
        """
        if _type == cls.DESIGNATOR.VENDOR_SPECIFIC:
            return data['vendor_specific']

        if _type == cls.DESIGNATOR.T10_VENDOR_ID:
            return data['t10_vendor_id'] + data['vendor_specific_id']

        if _type == cls.DESIGNATOR.EUI_64:
            if 'identifier_extension' in data:
                return data['identifier_extension'] + \
                    convert.scsi_int_to_ba(data['ieee_company_id'], 3) + \
                    data['vendor_specific_extension_id']
            if 'directory_id' in data:
                return convert.scsi_int_to_ba(data['ieee_company_id'], 3) + \
                    data['vendor_specific_extension_id'] + \
                    data['directory_id']

            return convert.scsi_int_to_ba(data['ieee_company_id'], 3) + \
                data['vendor_specific_extension_id']

        if _type == cls.DESIGNATOR.NAA:
            _r = bytearray(16)
            convert.decode_bits(data,
                                cls._naa_type_bits,
                                _r)
            if data['naa'] == cls.NAA.IEEE_EXTENDED:
                convert.encode_dict(data,
                                    cls._naa_ieee_extended_bits,
                                    _r)
                return _r[:8]
            if data['naa'] == cls.NAA.LOCALLY_ASSIGNED:
                convert.encode_dict(data,
                                    cls._naa_locally_assigned_bits,
                                    _r)
                return _r[:8]
            if data['naa'] == cls.NAA.IEEE_REGISTERED:
                convert.encode_dict(data,
                                    cls._naa_ieee_registered_bits,
                                    _r)
                return _r[:8]
            if data['naa'] == cls.NAA.IEEE_REGISTERED_EXTENDED:
                convert.encode_dict(data,
                                    cls._naa_ieee_registered_extended_bits,
                                    _r)
                return _r[:16]

        if _type == cls.DESIGNATOR.RELATIVE_TARGET_PORT_IDENTIFIER:
            _r = bytearray(4)
            convert.encode_dict(data,
                                cls._relative_port_bits,
                                _r)
            return _r

        if _type == cls.DESIGNATOR.TARGET_PORTAL_GROUP:
            _r = bytearray(4)
            convert.encode_dict(data,
                                cls._target_portal_group_bits,
                                _r)
            return _r

        if _type == cls.DESIGNATOR.LOGICAL_UNIT_GROUP:
            _r = bytearray(4)
            convert.encode_dict(data,
                                cls._logical_unit_group_bits,
                                _r)
            return _r

        if _type == cls.DESIGNATOR.MD5_LOGICAL_IDENTIFIER:
            return data['md5_logical_identifier']

        if _type == cls.DESIGNATOR.SCSI_NAME_STRING:
            return ['scsi_name_string']

        if _type == cls.DESIGNATOR.PCI_EXPRESS_ROUTING_ID:
            _r = bytearray(8)
            convert.encode_dict(data,
                                cls._pci_express_routing_id_bits,
                                _r)
            return _r

    @classmethod
    def marshall_designation_descriptor(cls,
                                        data):
        """
        static helper method to marshall designation desciptor data

        :param data: a dict with designator data
        :return: a byte array
        """
        _r = bytearray(4)
        convert.encode_dict(data,
                            cls._designator_bits,
                            _r)

        _r += cls.marshall_designator(data['designator_type'],
                                      data['designator'])
        _r[3] = len(_r) - 4
        return _r

    @classmethod
    def unmarshall_designator(cls,
                              _type,
                              data):
        """
        static helper method to unmarshall designator data

        :param _type: type of the designator
        :param data: a byte array with designator data
        :return: a dict
        """
        _d = {}
        if _type == cls.DESIGNATOR.VENDOR_SPECIFIC:
            _d['vendor_specific'] = data

        if _type == cls.DESIGNATOR.T10_VENDOR_ID:
            _d['t10_vendor_id'] = data[:8]
            _d['vendor_specific_id'] = data[8:]

        if _type == cls.DESIGNATOR.EUI_64:
            if len(data) == 8:
                _d['ieee_company_id'] = convert.scsi_ba_to_int(data[:3])
                _d['vendor_specific_extension_id'] = data[3:8]
            if len(data) == 12:
                _d['ieee_company_id'] = convert.scsi_ba_to_int(data[:3])
                _d['vendor_specific_extension_id'] = data[3:8]
                _d['directory_id'] = data[8:]
            if len(data) == 16:
                _d['identifier_extension'] = data[:8]
                _d['ieee_company_id'] = convert.scsi_ba_to_int(data[8:11])
                _d['vendor_specific_extension_id'] = data[11:]

        if _type == cls.DESIGNATOR.NAA:
            convert.decode_bits(data,
                                cls._naa_type_bits,
                                _d)
            if _d['naa'] == cls.NAA.IEEE_EXTENDED:
                convert.decode_bits(data,
                                    cls._naa_ieee_extended_bits,
                                    _d)
            if _d['naa'] == cls.NAA.LOCALLY_ASSIGNED:
                convert.decode_bits(data,
                                    cls._naa_locally_assigned_bits,
                                    _d)
            if _d['naa'] == cls.NAA.IEEE_REGISTERED:
                convert.decode_bits(data,
                                    cls._naa_ieee_registered_bits,
                                    _d)
            if _d['naa'] == cls.NAA.IEEE_REGISTERED_EXTENDED:
                convert.decode_bits(data,
                                    cls._naa_ieee_registered_extended_bits,
                                    _d)

        if _type == cls.DESIGNATOR.RELATIVE_TARGET_PORT_IDENTIFIER:
            convert.decode_bits(data,
                                cls._relative_port_bits,
                                _d)

        if _type == cls.DESIGNATOR.TARGET_PORTAL_GROUP:
            convert.decode_bits(data,
                                cls._target_portal_group_bits,
                                _d)

        if _type == cls.DESIGNATOR.LOGICAL_UNIT_GROUP:
            convert.decode_bits(data,
                                cls._logical_unit_group_bits,
                                _d)

        if _type == cls.DESIGNATOR.MD5_LOGICAL_IDENTIFIER:
            _d['md5_logical_identifier'] = data[0:16]

        if _type == cls.DESIGNATOR.SCSI_NAME_STRING:
            _d['scsi_name_string'] = data

        if _type == cls.DESIGNATOR.PCI_EXPRESS_ROUTING_ID:
            convert.decode_bits(data,
                                cls._pci_express_routing_id_bits,
                                _d)
        return _d

    @classmethod
    def unmarshall_ata_information(cls, data):
        result = {}
        _sig = data[36:41]
        _identify = data[44:]
        convert.decode_bits(data,
                            cls._ata_information_bits,
                            result)
        _r = {}
        convert.decode_bits(_sig,
                            cls._ata_signature_bits,
                            _r)
        result.update({'signature': _r})
        convert.decode_bits(_identify,
                            cls._ata_identify_bits,
                            _r)
        _gc = {}
        convert.decode_bits(_identify[:2],
                            cls._ata_identify_gen_conf_bits,
                            _gc)
        _r['general_config'] = _gc
        result.update({'identify': _r})
        return result

    @classmethod
    def unmarshall_datain(cls, data, evpd=0):
        """
        Unmarshall the Inquiry datain buffer

        :param data: a byte array with inquiry data
        :param evpd: evpd can be 0 or 1
        :return result: a dict
        """
        result = {}
        convert.decode_bits(data,
                            cls._datain_bits,
                            result)

        if evpd == 0:

            convert.decode_bits(data,
                                cls._standard_bits,
                                result)
            return result

        convert.decode_bits(data,
                            cls._pagecode_bits,
                            result)
        data = data[:4 + convert.scsi_ba_to_int(data[2:4])]
        if result['page_code'] == cls.VPD.SUPPORTED_VPD_PAGES:
            vpd_pages = []
            for i in data[4:]:
                vpd_pages.append(i)
            result.update({'vpd_pages': vpd_pages})
            return result

        if result['page_code'] == cls.VPD.BLOCK_LIMITS:
            convert.decode_bits(data,
                                cls._block_limits_bits,
                                result)
            return result

        if result['page_code'] == cls.VPD.BLOCK_DEVICE_CHARACTERISTICS:
            convert.decode_bits(data,
                                cls._block_dev_char_bits,
                                result)
            return result

        if result['page_code'] == cls.VPD.LOGICAL_BLOCK_PROVISIONING:
            convert.decode_bits(data,
                                cls._logical_block_provisioning_bits,
                                result)
            return result

        if result['page_code'] == cls.VPD.REFERRALS:
            convert.decode_bits(data,
                                cls._referrals_bits,
                                result)
            return result

        if result['page_code'] == cls.VPD.UNIT_SERIAL_NUMBER:
            result.update({'unit_serial_number': data[4:]})
            return result

        if result['page_code'] == cls.VPD.EXTENDED_INQUIRY_DATA:
            convert.decode_bits(data,
                                cls._extended_bits,
                                result)
            return result

        if result['page_code'] == cls.VPD.ATA_INFORMATION:
            result.update(cls.unmarshall_ata_information(data))
            return result

        if result['page_code'] == cls.VPD.DEVICE_IDENTIFICATION:
            data = data[4:]
            _d = []
            while len(data):
                _bc = data[3] + 4

                _dd = {}
                convert.decode_bits(data,
                                    cls._designator_bits,
                                    _dd)
                if _dd['piv'] == 0 or (_dd['association'] != 1 and _dd['association'] != 2):
                    del _dd['protocol_identifier']
                _dd['designator'] = cls.unmarshall_designator(_dd['designator_type'],
                                                              data[4:4 + data[3]])
                _d.append(_dd)
                data = data[_bc:]

            result.update({'designator_descriptors': _d})
            return result

    @classmethod
    def marshall_datain(cls, data):
        """
        Marshall the Inquiry datain.

        :param data: a dict with data
        :return result: a byte array
        """
        if 'page_code' not in data:
            result = bytearray(96)
            convert.encode_dict(data,
                                cls._datain_bits,
                                result)
            convert.encode_dict(data,
                                cls._standard_bits,
                                result)
            return result

        result = bytearray(4)
        convert.encode_dict(data,
                            cls._datain_bits,
                            result)
        convert.encode_dict(data,
                            cls._pagecode_bits,
                            result)
        if data['page_code'] == cls.VPD.LOGICAL_BLOCK_PROVISIONING:
            result += bytearray(4)
            convert.encode_dict(data,
                                cls._logical_block_provisioning_bits,
                                result)
        if data['page_code'] == cls.VPD.UNIT_SERIAL_NUMBER:
            result += data['unit_serial_number']
        if data['page_code'] == cls.VPD.REFERRALS:
            result += bytearray(12)
            convert.encode_dict(data,
                                cls._referrals_bits,
                                result)
        if data['page_code'] == cls.VPD.EXTENDED_INQUIRY_DATA:
            result += bytearray(60)
            convert.encode_dict(data,
                                cls._extended_bits,
                                result)
        if data['page_code'] == cls.VPD.DEVICE_IDENTIFICATION:
            for _dd in data['designator_descriptors']:
                _r = cls.marshall_designation_descriptor(_dd)
                result += _r

        result[2:4] = convert.scsi_int_to_ba(len(result) - 4, 2)
        return result
