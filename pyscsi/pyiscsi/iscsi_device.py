# coding: utf-8

# Copyright (C) 2018 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import pyscsi.pyscsi.scsi_enum_command as scsi_enum_command
from pyscsi.pyscsi.scsi_exception import SCSIDeviceCommandExceptionMeta as ExMETA

try:
    import iscsi
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
        self._iscsi = iscsi.Context(device)
        self._iscsi_url = iscsi.URL(self._iscsi, self._file_name)
        self._iscsi.set_targetname(self._iscsi_url.target)
        self._iscsi.set_session_type(iscsi.ISCSI_SESSION_NORMAL)
        self._iscsi.set_header_digest(iscsi.ISCSI_HEADER_DIGEST_NONE_CRC32C)
        self._iscsi.connect(self._iscsi_url.portal,
                            self._iscsi_url.lun)

    def close(self):
        self._iscsi.disconnect()

    def execute(self, cmd):
        """
        execute a scsi command
        :param cmd: a scsi command
        """
        dir = iscsi.SCSI_XFER_NONE
        xferlen = 0
        if len(cmd.datain):
            dir = iscsi.SCSI_XFER_READ
            xferlen = len(cmd.datain)
        if len(cmd.dataout):
            dir = iscsi.SCSI_XFER_WRITE
            xferlen = len(cmd.dataout)
        task = iscsi.Task(cmd.cdb, dir, xferlen)
        self._iscsi.command(
            self._iscsi_url.lun,
            task,
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
