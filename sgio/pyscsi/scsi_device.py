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

from scsi_exception import SCSIDeviceExceptionMeta as ExMETA


class SCSIDevice(object):
    """
    The base class for a derived  scsi device class

    """
    __metaclass__ = ExMETA

    def __init__(self, device):
        """
        initialize a  new instance

        :param device: the file descriptor
        """
        self._fd = sgio.open(device)

    def execute(self, cdb, dataout, datain, sense):
        """
        execute a scsi command

        :param cdb: a byte array representing a command descriptor block
        :param dataout: a byte array to hold received data from the ioctl call
        :param datain: a byte array to hold data passed to the ioctl call
        :param sense: a byte array to hold sense data
        """
        status = sgio.execute(self._fd, cdb, dataout, datain, sense)
        if status == scsi_enum_command.SCSI_STATUS.CHECK_CONDITION:
            raise SCSIDevice.CheckCondition(sense)
        if status == scsi_enum_command.SCSI_STATUS.SGIO_ERROR:
            raise SCSIDevice.SCSISGIOError

