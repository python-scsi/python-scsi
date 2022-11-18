# coding: utf-8

# Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
# SPDX-FileCopyrightText: 2014 The python-scsi Authors
#
# SPDX-License-Identifier: LGPL-2.1-or-later

import os

import pyscsi.pyscsi.scsi_enum_command as scsi_enum_command
from pyscsi.pyscsi.scsi_exception import SCSIDeviceCommandExceptionMeta as ExMETA

try:
    import sgio
    _has_sgio = True
except ImportError as e:
    _has_sgio = False


def get_inode(file):
    #  type: (str) -> int
    return os.stat(file).st_ino


class SCSIDevice(metaclass=ExMETA):
    """
    The scsi device class

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
                 device,
                 readwrite=False,
                 detect_replugged=True):
        """
        initialize a  new instance of a SCSIDevice
        :param device: the file descriptor
        :param readwrite: access type
        :param detect_replugged: detects device unplugged and plugged events and ensure executions will not fail
        silently due to replugged events
        """
        self._opcodes = scsi_enum_command.spc
        self._file_name = device
        self._read_write = readwrite
        self._file = None
        self._ino = None
        self._detect_replugged = detect_replugged

        if _has_sgio and device[:5] == '/dev/':
            self.open()
        else:
            raise NotImplementedError('No backend implemented for %s' % device)

    def __enter__(self):
        """

        :return:
        """
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
        self.close()

    def __repr__(self):
        """

        :return:
        """
        return self.__class__.__name__

    def _is_replugged(self):
        #  type: (SCSIDevice) -> bool
        ino = get_inode(self._file_name)
        return ino != self._ino

    def open(self):
        """

        :param dev:
        :param read_write:
        :return:
        """
        self._file = open(self._file_name,
                          'w+b' if self._read_write else 'rb')
        self._ino = get_inode(self._file_name)

    def close(self):
        self._file.close()

    def execute(self, cmd):
        """
        execute a scsi command

        :param cmd: a SCSICommand
        """
        if self._detect_replugged and self._is_replugged():
            try:
                self.close()
            finally:
                self.open()

        try:
            sgio.execute(
                self._file,
                cmd.cdb,
                cmd.dataout,
                cmd.datain)
        except sgio.CheckConditionError as error:
            self.CheckCondition(error.sense)

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
