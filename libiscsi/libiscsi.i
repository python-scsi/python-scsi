/*
   Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU Lesser General Public License as published by
   the Free Software Foundation; either version 2.1 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public License
   along with this program; if not, see <http://www.gnu.org/licenses/>.
*/

%module libiscsi

/* Include start*/

%{
#include <iscsi/iscsi.h>
#include <iscsi/scsi-lowlevel.h>
%}

%include <stdint.i>

/* Include end*/

/* Typemap start */

%typemap(in) (int cdb_size, unsigned char *cdb)
  (int res, Py_ssize_t size = 0, const void *buf = 0) {
  res = PyObject_AsReadBuffer($input, &buf, &size);
  if (res<0) {
    PyErr_Clear();
    %argument_fail(res, "(TYPEMAP, SIZE)", $symname, $argnum);
  }
  $2 = ($2_ltype) buf;
  $1 = ($1_ltype) (size/sizeof($*2_type));
}
%typemap(in) (int len, unsigned char *rw)
  (int res, Py_ssize_t size = 0, void *buf = 0) {
  res = PyObject_AsWriteBuffer($input, &buf, &size);
  if (res<0) {
    PyErr_Clear();
    %argument_fail(res, "(TYPEMAP, SIZE)", $symname, $argnum);
  }
  $2 = ($2_ltype) buf;
  $1 = ($1_ltype) (size/sizeof($*2_type));
}
%typemap(in) (int len, unsigned char *ro)
  (int res, Py_ssize_t size = 0, const void *buf = 0) {
  res = PyObject_AsReadBuffer($input, &buf, &size);
  if (res<0) {
    PyErr_Clear();
    %argument_fail(res, "(TYPEMAP, SIZE)", $symname, $argnum);
  }
  $2 = ($2_ltype) buf;
  $1 = ($1_ltype) (size/sizeof($*2_type));
}
%typemap(in) (unsigned char *ro, uint32_t len)
  (int res, Py_ssize_t size = 0, const void *buf = 0) {
  res = PyObject_AsReadBuffer($input, &buf, &size);
  if (res<0) {
    PyErr_Clear();
    %argument_fail(res, "(TYPEMAP, SIZE)", $symname, $argnum);
  }
  $1 = ($1_ltype) buf;
  $2 = ($2_ltype) (size/sizeof($1_type));
}

/* Typemap end*/

/* DEFINE start */

#define MAX_STRING_SIZE (255)

/* DEFINE end */

/* enum start*/

enum iscsi_immediate_data {
	ISCSI_IMMEDIATE_DATA_NO  = 0,
	ISCSI_IMMEDIATE_DATA_YES = 1
};

enum iscsi_initial_r2t {
	ISCSI_INITIAL_R2T_NO  = 0,
	ISCSI_INITIAL_R2T_YES = 1
};

enum iscsi_session_type {
	ISCSI_SESSION_DISCOVERY = 1,
	ISCSI_SESSION_NORMAL    = 2
};

enum iscsi_header_digest {
	ISCSI_HEADER_DIGEST_NONE        = 0,
	ISCSI_HEADER_DIGEST_NONE_CRC32C = 1,
	ISCSI_HEADER_DIGEST_CRC32C_NONE = 2,
	ISCSI_HEADER_DIGEST_CRC32C      = 3,
	ISCSI_HEADER_DIGEST_LAST        = ISCSI_HEADER_DIGEST_CRC32C
};

enum scsi_xfer_dir {
	SCSI_XFER_NONE  = 0,
	SCSI_XFER_READ  = 1,
	SCSI_XFER_WRITE = 2
};

/* enum end*/

/* struct start*/

struct iscsi_context;
struct scsi_task;
struct iscsi_url {
       char portal[MAX_STRING_SIZE + 1];
       char target[MAX_STRING_SIZE + 1];
       char user[MAX_STRING_SIZE + 1];
       char passwd[MAX_STRING_SIZE + 1];
       int lun;
       struct iscsi_context *iscsi;
};
struct iscsi_data {
       size_t size;
       unsigned char *data;
};

/* struct end*/

/* function start*/

extern struct iscsi_context *iscsi_create_context(const char *initiator_name);
extern int iscsi_set_alias(struct iscsi_context *iscsi,
                           const char *alias);
extern int iscsi_set_session_type(struct iscsi_context *iscsi,
                                  enum iscsi_session_type session_type);
extern int iscsi_set_header_digest(struct iscsi_context *iscsi,
                                   enum iscsi_header_digest header_digest);
extern int iscsi_full_connect_sync(struct iscsi_context *iscsi,
                                   const char *portal, int lun);
extern int iscsi_destroy_context(struct iscsi_context *iscsi);
extern struct iscsi_url *iscsi_parse_full_url(struct iscsi_context *iscsi,
                                              const char *url);
extern int iscsi_set_targetname(struct iscsi_context *iscsi,
                                const char *targetname);
extern struct scsi_task *iscsi_scsi_command_sync(struct iscsi_context *iscsi,
                                                 int lun,
			                                     struct scsi_task *task,
			                                     struct iscsi_data *data);
extern struct scsi_task *scsi_create_task(int cdb_size,
                                          unsigned char *cdb,
                                          int xfer_dir,
                                          int expxferlen);
extern int scsi_task_add_data_in_buffer(struct scsi_task *task,
                                        int len,
                                        unsigned char *rw);
extern int scsi_task_add_data_out_buffer(struct scsi_task *task,
                                         int len,
                                         unsigned char *ro);
extern int scsi_task_get_status(struct scsi_task *task,
                                struct scsi_sense *sense);

//extern const char *iscsi_url_target_get(struct iscsi_url *url);

/* function end */
