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

    cdef struct scsi_task:
        pass

    cdef struct scsi_sense:
        pass

    scsi_task *scsi_create_task(
        int cdb_size, unsigned char *cdb, int xfer_dir, int expxferlen)


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

    cdef struct iscsi_data:
        pass

    cdef iscsi_context *iscsi_create_context(const char *initiator_name)
    cdef iscsi_url *iscsi_parse_full_url(iscsi_context *iscsi, const char* url)
    cdef int iscsi_set_targetname(iscsi_context *iscsi, const char *targetname)
    cdef int iscsi_set_session_type(iscsi_context *iscsi, iscsi_session_type session_type)
    cdef int iscsi_set_header_digest(iscsi_context *iscsi, iscsi_header_digest header_digest)
    cdef int iscsi_full_connect_sync(iscsi_context *iscsi, const char *portal, int lun)
    cdef int iscsi_disconnect(iscsi_context *iscsi)

    cdef scsi_task_add_data_in_buffer(scsi_task *task, int len, unsigned char *buf)
    cdef scsi_task_add_data_out_buffer(scsi_task *task, int len, unsigned char *buf)

    cdef scsi_task *iscsi_scsi_command_sync(
        iscsi_context *iscsi, int lun, scsi_task *task, iscsi_data *data)
    cdef int scsi_task_get_status(scsi_task *task, scsi_sense *sense)


cdef class Task:
    cdef scsi_task *_task
    cdef bint _has_datain
    cdef unsigned char[:] _datain_view
    cdef bint _has_dataout
    cdef unsigned char[:] _dataout_view

    def __init__(self, bytes cdb, scsi_xfer_dir direction, size_t xferlen):
        self._task = scsi_create_task(len(cdb), cdb, direction, xferlen)
        self._has_datain = False
        self._has_dataout = False

    @property
    def status(self):
        return scsi_task_get_status(self._task, NULL)


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

    def command(self, int lun, Task task, bytearray data_out, bytearray data_in):
        # Get the data in/out bytearrays here so that Python can't change them.
        cdef unsigned char[:] data_out_view = data_out
        cdef unsigned char[:] data_in_view = data_in

        if len(data_out):
            scsi_task_add_data_out_buffer(task._task, len(data_out), &data_out_view[0])
        if len(data_in):
            scsi_task_add_data_in_buffer(task._task, len(data_in), &data_in_view[0])

        iscsi_scsi_command_sync(self._ctx, lun, task._task, NULL)


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
