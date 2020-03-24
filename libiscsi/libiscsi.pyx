# 
#  Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
#  Copyright (C) 2020 by Diego Elio Pettenò <flameeyes@flameeyes.com>
# 
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
# 
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.
#

from libc.stdlib cimport calloc

cdef extern from "iscsi/scsi-lowlevel.h":
    cpdef enum scsi_xfer_dir:
        SCSI_XFER_NONE
        SCSI_XFER_READ
        SCSI_XFER_WRITE


cdef extern from "iscsi/iscsi.h":
    cpdef enum iscsi_immediate_data:
        ISCSI_IMMEDIATE_DATA_NO
        ISCSI_IMMEDIATE_DATA_YES

    cpdef enum iscsi_initial_r2t:
        ISCSI_INITIAL_R2T_NO
        ISCSI_INITIAL_R2T_YES

    cpdef enum iscsi_session_type:
        ISCSI_SESSION_DISCOVERY
        ISCSI_SESSION_NORMAL

    cpdef enum iscsi_header_digest:
        ISCSI_HEADER_DIGEST_NONE
        ISCSI_HEADER_DIGEST_NONE_CRC32C
        ISCSI_HEADER_DIGEST_CRC32C_NONE
        ISCSI_HEADER_DIGEST_CRC32C
        ISCSI_HEADER_DIGEST_LAST

    cdef struct iscsi_context:
        pass

    cdef struct iscsi_url:
        char portal[256]
        char target[256]
        char user[256]
        char passwd[256]
        int lun
        iscsi_context *iscsi

    cdef struct scsi_task:
        pass

    cdef struct iscsi_data:
        size_t size
        unsigned char *data

    cdef iscsi_context *iscsi_create_context(const char *initiator_name)
    cdef iscsi_url *iscsi_parse_full_url(iscsi_context *iscsi, const char* url)
    cdef int iscsi_set_targetname(iscsi_context *iscsi, const char *targetname)
    cdef int iscsi_set_session_type(iscsi_context *iscsi, iscsi_session_type session_type)
    cdef int iscsi_set_header_digest(iscsi_context *iscsi, iscsi_header_digest header_digest)
    cdef int iscsi_full_connect_sync(iscsi_context *iscsi, const char *portal, int lun)
    cdef int iscsi_disconnect(iscsi_context *iscsi)


cdef class Context:
    cdef iscsi_context *_ctx

    def __init__(self, str initiator_name):
        self._ctx = iscsi_create_context(initiator_name.encode('utf-8'))
        if not self._ctx:
            raise ValueError("Invalid initiator name: %s" % initiator_name)

    def set_targetname(self, str targetname):
        if iscsi_set_targetname(self._ctx, targetname.encode('utf-8')) < 0:
            raise ValueError("Invalid target name: %s" % targetname)

    def set_session_type(self, iscsi_session_type session_type):
        if iscsi_set_session_type(self._ctx, session_type) < 0:
            raise ValueError("Invalid session type: %s" % session_type)

    def set_header_digest(self, iscsi_header_digest header_digest):
        if iscsi_set_header_digest(self._ctx, header_digest) < 0:
            raise ValueError("Invalid header digest: %s" % header_digest)

    def connect(self, str portal, int lun):
        if iscsi_full_connect_sync(self._ctx, portal.encode('utf-8'), lun) < 0:
            raise RuntimeError("Unable to connect to %s" % portal)

    def disconnect(self):
        if iscsi_disconnect(self._ctx) < 0:
            raise RuntimeError("Disconnection error.")


cdef class URL:
    cdef iscsi_url *_url

    def __init__(self, Context ctx, str url_str):
        self._url = iscsi_parse_full_url(ctx._ctx, url_str.encode('utf-8'))
        if not self._url:
            raise ValueError("URL parsing failed: %s" % url_str)

    @property
    def portal(self):
        return self._url.portal.decode('utf-8')

    @property
    def target(self):
        return self._url.target.decode('utf-8')

    @property
    def user(self):
        return self._url.user.decode('utf-8')

    @property
    def passwd(self):
        return self._url.passwd.decode('utf-8')

    @property
    def lun(self):
        return self._url.lun
