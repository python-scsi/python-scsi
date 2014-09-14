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

class SCSICommand:
    '''

    '''
    def __init__(self, dev, dataout_alloclen, datain_alloclen):
        '''

        :param dev:
        :param dataout_alloclen:
        :param datain_alloclen:
        :return:
        '''
        self.dev = dev
        self.sense = bytearray(32)
        self.dataout = bytearray(dataout_alloclen)
        self.datain = bytearray(datain_alloclen)
        self._result = {}

    def execute(self):
        '''

        :return:
        '''
        self.dev.execute(self.cdb, self.dataout,
                         self.datain, self.sense)
        self.unmarshall()

    @property
    def result(self):
        '''

        :return:
        '''
        return self._result

    @result.setter
    def result(self, value):
        '''

        :param value:
        :return:
        '''
        self._result = value

    def add_result(self, key, value):
        '''

        :param key:
        :param value:
        :return:
        '''
        self.result.update({key:value})
