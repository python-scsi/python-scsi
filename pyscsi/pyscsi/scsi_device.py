# coding: utf-8


# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
import pyscsi.pyscsi.scsi_enum_command as scsi_enum_command

from pyscsi.pyscsi.scsi_exception import SCSIDeviceCommandExceptionMeta as ExMETA

try:
    import libiscsi
    _have_libiscsi = True
except ImportError as e:
    _have_libiscsi = False

try:
    import linux_sgio
    _have_linux_sgio = True
except ImportError as e:
    _have_linux_sgio = False

# make a new base class with the metaclass this should solve the problem with the
# python 2 and python 3 metaclass definitions
_new_base_class = ExMETA('SCSIDeviceCommandExceptionMeta', (object,), {})


class SCSIDevice(_new_base_class):
    """
    The base class for a derived  scsi device class
    """

    def __init__(self, device, readwrite=False):
        """
        initialize a  new instance

        :param device: the file descriptor
        :param readwrite: access type
        """
        self._is_libiscsi = False
        self._is_linux_sgio = False
        self._opcodes = scsi_enum_command.spc

        if _have_libiscsi and device[:8] == 'iscsi://':
            self._iscsi = libiscsi.iscsi_create_context('iqn.2007-10.com.github:python-scsi')
            self._iscsi_url = libiscsi.iscsi_parse_full_url(self._iscsi, device)
            libiscsi.iscsi_set_targetname(self._iscsi, self._iscsi_url.target)
            libiscsi.iscsi_set_session_type(self._iscsi, libiscsi.ISCSI_SESSION_NORMAL)
            libiscsi.iscsi_set_header_digest(self._iscsi, libiscsi.ISCSI_HEADER_DIGEST_NONE_CRC32C)
            libiscsi.iscsi_full_connect_sync(self._iscsi, self._iscsi_url.portal, self._iscsi_url.lun)

            self._is_libiscsi = True
        elif _have_linux_sgio and device[:5] == '/dev/':
            self._is_linux_sgio = True
            self._fd = linux_sgio.open(device, bool(readwrite))
        else:
            raise NotImplementedError('No backend implemented for %s' % device)

    def execute(self, cdb, dataout, datain, sense):
        """
        execute a scsi command

        :param cdb: a byte array representing a command descriptor block
        :param dataout: a byte array to hold received data from the ioctl call
        :param datain: a byte array to hold data passed to the ioctl call
        :param sense: a byte array to hold sense data
        """
        if self.isLibSCSI:
            _dir = libiscsi.SCSI_XFER_NONE
            _xferlen = 0
            if len(datain):
                _dir = libiscsi.SCSI_XFER_READ
                _xferlen = len(datain)
            if len(dataout):
                _dir = libiscsi.SCSI_XFER_WRITE
                _xferlen = len(dataout)
            _task = libiscsi.scsi_create_task(cdb, _dir, _xferlen)
            if len(datain):
                libiscsi.scsi_task_add_data_in_buffer(_task, datain)
            if len(dataout):
                libiscsi.scsi_task_add_data_out_buffer(_task, dataout)

            libiscsi.iscsi_scsi_command_sync(self._iscsi, self._iscsi_url.lun, _task, None)
            _status = libiscsi.scsi_task_get_status(_task, None)
            if _status == libiscsi.SCSI_STATUS_CHECK_CONDITION:
                raise self.CheckCondition(sense)
            if _status == libiscsi.SCSI_STATUS_GOOD:
                return

            raise self.SCSISGIOError

        elif self.isLinuxSGIO:
            _dir = linux_sgio.DXFER_NONE
            if len(datain) and len(dataout):
                raise NotImplemented('Indirect IO is not supported')
            elif len(datain):
                _dir = linux_sgio.DXFER_FROM_DEV
            elif len(dataout):
                _dir = linux_sgio.DXFER_TO_DEV

            status = linux_sgio.execute(self._fd, _dir, cdb, dataout, datain, sense)
            if status == scsi_enum_command.SCSI_STATUS.CHECK_CONDITION:
                raise self.CheckCondition(sense)
            if status == scsi_enum_command.SCSI_STATUS.SGIO_ERROR:
                raise self.SCSISGIOError

    @property
    def isLibSCSI(self):
        return self._is_libiscsi

    @isLibSCSI.setter
    def isLibSCSI(self, value):
        self._is_libiscsi = value

    @property
    def isLinuxSGIO(self):
        return self._is_linux_sgio

    @isLinuxSGIO.setter
    def isLinuxSGIO(self, value):
        self._is_linux_sgio = value

    @property
    def opcodes(self):
        return self._opcodes

    @opcodes.setter
    def opcodes(self, value):
        self._opcodes = value

    @property
    def devicetype(self):
        return self._devicetype

    @devicetype.setter
    def devicetype(self, value):
        self._devicetype = value
