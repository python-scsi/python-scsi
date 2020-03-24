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


try:
    import libiscsi
    _has_iscsi = True
except ImportError as e:
    _has_iscsi = False


class ISCSIDevice(metaclass=ExMETA):
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
        self._iscsi = libisci.Context(device)
        self._iscsi_url = libiscsi.URL(self._iscsi, self._file_name)
        self._iscsi.set_targetname(self._iscsi_url.target)
        self._iscsi.set_session_type(libiscsi.ISCSI_SESSION_NORMAL)
        self._iscsi.set_header_digest(libiscsi.ISCSI_HEADER_DIGEST_NONE_CRC32C)
        self._iscsi.full_connect_sync(self._iscsi_url.portal,
                                       self._iscsi_url.lun)

    def close(self):
        self._iscsi.disconnect()

    def execute(self, cmd):
        """
        execute a scsi command
        :param cmd: a scsi command
        """
        dir = libiscsi.SCSI_XFER_NONE
        xferlen = 0
        if len(cmd.datain):
            dir = libiscsi.SCSI_XFER_READ
            xferlen = len(cmd.datain)
        if len(cmd.dataout):
            dir = libiscsi.SCSI_XFER_WRITE
            xferlen = len(cmd.dataout)
        task = libiscsi.Task(cmd.cdb, dir, xferlen)
        self._iscsi.command(
            self._iscsi_url.lun,
            _task,
            cmd.dataout,
            cmd.datain)
        if task.status == scsi_enum_command.SCSI_STATUS.CHECK_CONDITION:
            # No sense information propagated.
            raise self.CheckCondition(cmd.sense)
        if task.status == scsi_enum_command.SCSI_STATUS.GOOD:
            return
        raise RuntimeError

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
