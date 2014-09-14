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

import scsi
import scsi_sense
import sgio

class SCSIDevice:
    '''

    '''
    def __init__(self, device):
        '''

        :param device:
        :return:
        '''
        self._fd = sgio.open(device)

    def execute(self, cdb, dataout, datain, sense):
        '''

        :param cdb:
        :param dataout:
        :param datain:
        :param sense:
        :return:
        '''
        status = sgio.execute(self._fd, cdb, dataout, datain, sense)
        if status == scsi.SCSI_STATUS_CHECK_CONDITION:
            raise scsi_sense.SCSICheckCondition(sense)
        if status == scsi.SCSI_STATUS_SGIO_ERROR:
            raise scsi_sense.SCSISGIOError()

