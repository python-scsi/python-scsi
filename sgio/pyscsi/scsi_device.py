# coding: utf-8


#      Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
#
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU Lesser General Public License as published by
#	   the Free Software Foundation; either version 2.1 of the License, or
#	   (at your option) any later version.
#
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU Lesser General Public License for more details.
#
#	   You should have received a copy of the GNU Lesser General Public License
#	   along with this program; if not, see <http://www.gnu.org/licenses/>.

import scsi_enum_command
import sgio
try:
    import libiscsi
    _have_libiscsi = True
except:
    _have_libiscsi = False

from scsi_exception import SCSIDeviceExceptionMeta as ExMETA


class SCSIDevice(object):
    """
    The base class for a derived scsi device class.

    """
    __metaclass__ = ExMETA

    def __init__(self, device, readwrite=False):
        """
        Open and initialize a new sg device instance.

        :param device:    The pathname of the device to open.

        :param readwrite: If False (default) the device will be opened in
                          read-only mode, otherwise it will be opened in
                          read/write mode.
        """
        self._fd = sgio.open(device)

            self._is_libiscsi = True
        else:
            self._fd = sgio.open(device)

    def execute(self, cdb, dataout, datain, sense):
        """
        execute a scsi command

        :param cdb: a byte array representing a command descriptor block
        :param dataout: a byte array to hold received data from the ioctl call
        :param datain: a byte array to hold data passed to the ioctl call
        :param sense: a byte array to hold sense data
        """
        if self._is_libiscsi:
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
                raise SCSIDevice.CheckCondition(sense)
            if _status == libiscsi.SCSI_STATUS_GOOD:
                return

            raise SCSIDevice.SCSISGIOError

        else:
            status = sgio.execute(self._fd, cdb, dataout, datain, sense)
            if status == scsi_enum_command.SCSI_STATUS.CHECK_CONDITION:
                raise SCSIDevice.CheckCondition(sense)
            if status == scsi_enum_command.SCSI_STATUS.SGIO_ERROR:
                raise SCSIDevice.SCSISGIOError

