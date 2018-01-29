# coding: utf-8

# Copyright:
#  Copyright (C) 2018 by Markus Rosjat<markus.rosjat@gmail.com>
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

from pyscsi.pyscsi.scsi_exception import SCSIDeviceCommandExceptionMeta as ExMETA
import pyscsi.pyscsi.scsi_enum_command as scsi_enum_command
from pyscsi.pyiscsi.iscsi_url import ISCSIUrl


try:
    import libiscsi._libiscsi as _iscsi
    _has_iscsi = True
except ImportError as e:
    _has_iscsi = False

# make a new base class with the metaclass this should solve the problem with the
# python 2 and python 3 metaclass definitions
_new_base_class = ExMETA('SCSIDeviceCommandExceptionMeta', (object,), {})


class ISCSIDevice(_new_base_class):
    """
    The iscsi device class

    By default it gets the SPC opcodes assigned so it's always possible to issue
    a inquiry command to the device. This is important since the the Command will
    figure out the opcode from the SCSIDevice first to use it for building the cdb.
    This means after the that it's possible to use the proper OpCodes for the device.
    A basic workflow for using a device would be:
        - try to open the device passed by the device arg
        - create a  Inquiry instance, with the default opcodes of the device
        - execute the inquiry with the device
        - unmarshall the datain from the inquiry command to figure out the device type
        - assign the proper Opcode for the device type (it would also work just to use the
          opcodes without assigning them to the device since the command builds the cdb
          and the device just executes)

    Note: The workflow above is already implemented in the SCSI class
    """

    def __init__(self,
                 device):
        """
        initialize a  new instance of a ISCSIDevice

        :param device: a url string
        """
        self._opcodes = scsi_enum_command.spc
        self._file_name = device
        self._iscsi = None
        self._iscsi_url = None
        if _has_iscsi and device[:8] == 'iscsi://':
            self.open(device)
        else:
            raise NotImplementedError('No backend implemented for %s' % device)

    def __enter__(self):
        return self

    def __exit__(self,
                 exc_type,
                 exc_val,
                 exc_tb):
        """

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        # we may need to do more teardown here ?
        self.close()

    def open(self, device):
        """

        """
        self._iscsi = _iscsi.iscsi_create_context(device)
        self._iscsi_url = ISCSIUrl(self._iscsi,
                                   self._file_name)
        _iscsi.iscsi_set_targetname(self._iscsi,
                                    self._iscsi_url.target)
        _iscsi.iscsi_set_session_type(self._iscsi,
                                        _iscsi.ISCSI_SESSION_NORMAL)
        _iscsi.iscsi_set_header_digest(self._iscsi,
                                         _iscsi.ISCSI_HEADER_DIGEST_NONE_CRC32C)
        _iscsi.iscsi_full_connect_sync(self._iscsi,
                                       self._iscsi_url.portal,
                                       self._iscsi_url.lun)

    def close(self):
        # we may need to do more teardown here ?
        _iscsi.iscsi_destroy_context(self._iscsi)

    def execute(self, cmd):
        """
        execute a scsi command
        :param cmd: a scsi command
        """
        _dir = _iscsi.SCSI_XFER_NONE
        _xferlen = 0
        if len(cmd.datain):
            _dir = _iscsi.SCSI_XFER_READ
            _xferlen = len(cmd.datain)
        if len(cmd.dataout):
            _dir = _iscsi.SCSI_XFER_WRITE
            _xferlen = len(cmd.dataout)
        _task = _iscsi.scsi_create_task(cmd.cdb,
                                          _dir,
                                          _xferlen)
        if len(cmd.datain):
            _iscsi.scsi_task_add_data_in_buffer(_task,
                                                cmd.datain)
        if len(cmd.dataout):
            _iscsi.scsi_task_add_data_out_buffer(_task,
                                                 cmd.dataout)
        _iscsi.iscsi_scsi_command_sync(self._iscsi,
                                       self._iscsi_url.lun,
                                         _task,
                                         None)
        _status = _iscsi.scsi_task_get_status(_task,
                                                None)
        if _status == scsi_enum_command.SCSI_STATUS.CHECK_CONDITION:
            raise self.CheckCondition(cmd.sense)
        if _status == scsi_enum_command.SCSI_STATUS.GOOD:
            return
        raise self.SCSISGIOError

    @property
    def opcodes(self):
        return self._opcodes

    @opcodes.setter
    def opcodes(self,
                value):
        self._opcodes = value

    @property
    def devicetype(self):
        return self._devicetype

    @devicetype.setter
    def devicetype(self,
                   value):
        self._devicetype = value
