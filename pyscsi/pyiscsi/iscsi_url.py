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

import libiscsi._libiscsi as _iscsi


class ISCSIUrl(object):
    """
    Wrapperclass for a iscsi_url struct.

    SWIG does a lot of weird stuff in the python code it creates to make
    a new instance of the iscsi_url struct so some things might break with
    the simple approach of calling new_iscsi_url and delete_iscsi_url

    NOTE: PYSCSI will create an instance of this class by
          calling parse_full_url!

    """
    def __init__(self, context, url_str=None):
        """

        :param context:
        :param url_str:
        """
        if url_str:
            self._url = _iscsi.iscsi_parse_full_url(context, url_str)
        else:
            self._url = _iscsi.new_iscsi_url()

    @property
    def lun(self):
        """
        Get the lun from the url.

        """
        return _iscsi.iscsi_url_lun_get(self._url)

    @lun.setter
    def lun(self, lun):
        """

        :param lun:
        """
        _iscsi.iscsi_url_lun_set(self._url, lun)

    @property
    def portal(self):
        """
        Get the portal from the url.

        :return: a string
        """
        return _iscsi.iscsi_url_portal_get(self._url)

    @portal.setter
    def portal(self, portal):
        """
        Set the portal on the url.

        :param portal: a string
        """
        _iscsi.iscsi_url_portal_set(self._url, portal)

    @property
    def target(self):
        """
        Get the target from the url.

        :return: a string
        """
        return _iscsi.iscsi_url_target_get(self._url)

    @target.setter
    def target(self, target):
        """
        Set the target on the url.

        :param target: a string
        """
        _iscsi.iscsi_url_target_set(self._url, target)

    @property
    def user(self):

        return _iscsi.iscsi_url_user_get(self._url)

    @user.setter
    def user(self, user):
        return _iscsi.iscsi_url_user_set(self._url, user)

    @property
    def password(self):
        return _iscsi.iscsi_url_passwd_get(self._url)

    @password.setter
    def password(self, passwd):
        return _iscsi.iscsi_url_passwd_set(self._url, passwd)

    @property
    def iscsi(self):
        return _iscsi.iscsi_url_iscsi_get(self._url)

    @iscsi.setter
    def iscsi(self, target):
        return _iscsi.iscsi_url_iscsi_set(self._url, target)

    def __del__(self):
        _iscsi.delete_iscsi_url(self._url)

