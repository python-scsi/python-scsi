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

#define _GNU_SOURCE
#include <stdio.h>

#include <iscsi/iscsi.h>
#include <iscsi/scsi-lowlevel.h>

#include <sys/syscall.h>
#include <dlfcn.h>
#include <inttypes.h>

#include <Python.h>

static void *libiscsi_handle;
static struct iscsi_context *(*dl_iscsi_create_context)(__const char *initiator);
static int (*dl_iscsi_destroy_context)(struct iscsi_context *iscsi);
static char *(*dl_iscsi_get_error)(struct iscsi_context *iscsi);
static struct iscsi_url *(*dl_iscsi_parse_full_url)(struct iscsi_context *iscsi, __const char *url);
static void (*dl_iscsi_destroy_url)(struct iscsi_url *url);
static int (*dl_iscsi_set_targetname)(struct iscsi_context *iscsi, __const char *target);
static int (*dl_iscsi_set_session_type)(struct iscsi_context *iscsi, enum iscsi_session_type session_type);
static int (*dl_iscsi_set_header_digest)(struct iscsi_context *iscsi, enum iscsi_header_digest header_digest);
static int (*dl_iscsi_full_connect_sync)(struct iscsi_context *iscsi, const char *portal, int lun);
static struct scsi_task *(*dl_iscsi_scsi_command_sync)(struct iscsi_context *iscsi, int lun, struct scsi_task *task, struct iscsi_data *data);

static PyObject *LibiscsiError;

struct iscsi_wrapper {
  struct iscsi_context *iscsi;
  struct iscsi_url *iscsi_url;
};

static PyObject *
libiscsi_open(PyObject *self, PyObject *args)
{
  const char *url;
  struct iscsi_wrapper *iw;

  if (!PyArg_ParseTuple(args, "s", &url))
    return NULL;

  iw = malloc(sizeof(struct iscsi_wrapper));
  if (iw == NULL) {
    PyErr_SetString(LibiscsiError, "Failed to allocate iscsi wrapper.");
    return NULL;
  }

  iw->iscsi = dl_iscsi_create_context("iqn.2007-10.com.github:sahlberg:python-libiscsi");
  if (iw->iscsi == NULL) {
    PyErr_SetString(LibiscsiError, "Failed to create iSCSI context.");
    free(iw);
    return NULL;
  }

  iw->iscsi_url = dl_iscsi_parse_full_url(iw->iscsi, url);
  if (iw->iscsi_url == NULL) {
    PyErr_SetString(LibiscsiError, "Failed to parse iSCSI url.");
    dl_iscsi_destroy_context(iw->iscsi);
    free(iw);
    return NULL;
  }

  dl_iscsi_set_targetname(iw->iscsi, iw->iscsi_url->target);
  dl_iscsi_set_session_type(iw->iscsi, ISCSI_SESSION_NORMAL);
  dl_iscsi_set_header_digest(iw->iscsi, ISCSI_HEADER_DIGEST_NONE_CRC32C);

  if (dl_iscsi_full_connect_sync(iw->iscsi, iw->iscsi_url->portal, iw->iscsi_url->lun) != 0) {
    char *str;
    asprintf(&str, "Failed to connect to iSCSI URL: %s", dl_iscsi_get_error(iw->iscsi));
    PyErr_SetString(LibiscsiError, str);
    free(str);
    dl_iscsi_destroy_url(iw->iscsi_url);
    dl_iscsi_destroy_context(iw->iscsi);
    free(iw);
    return NULL;
  }

  return Py_BuildValue("K", (unsigned long long)iw);
}

static PyObject *
libiscsi_execute(PyObject *self, PyObject *args)
{
  unsigned long long tiw;
  struct iscsi_wrapper *iw;
  struct scsi_task *task;
  struct iscsi_data *data = NULL, d;
  PyObject *cdb_arg, *dataout_arg, *datain_arg, *sense_arg;
  Py_buffer cdb_buf, dataout_buf, datain_buf, sense_buf;

  if (!PyArg_ParseTuple(args, "KOOOO:sgio_execute",
			&tiw,
			&cdb_arg, &dataout_arg, &datain_arg, &sense_arg))
    return NULL;
  if (PyObject_GetBuffer(cdb_arg, &cdb_buf, PyBUF_WRITABLE) < 0)
    return NULL;
  if (PyObject_GetBuffer(dataout_arg, &dataout_buf, PyBUF_WRITABLE) < 0)
    return NULL;
  if (PyObject_GetBuffer(datain_arg, &datain_buf, PyBUF_WRITABLE) < 0)
    return NULL;
  if (PyObject_GetBuffer(sense_arg, &sense_buf, PyBUF_WRITABLE) < 0)
    return NULL;

  iw = (struct iscsi_wrapper *)tiw;
  task = malloc(sizeof(struct scsi_task));
  if (task == NULL)
    return NULL;

  memset(task, 0, sizeof(struct scsi_task));
  task->xfer_dir = SCSI_XFER_NONE;
  if (dataout_buf.len) {
    task->xfer_dir = SCSI_XFER_WRITE;
    task->expxferlen = dataout_buf.len;
    data = &d;
    data->size = dataout_buf.len;
    data->data = dataout_buf.buf;
  }
  if (datain_buf.len) {
    task->xfer_dir = SCSI_XFER_READ;
    task->expxferlen = datain_buf.len;
    data = &d;
    data->size = datain_buf.len;
    data->data = datain_buf.buf;
  }
  task->cdb_size = cdb_buf.len;
  memcpy(&task->cdb[0], cdb_buf.buf, cdb_buf.len);

  if (dl_iscsi_scsi_command_sync(iw->iscsi, iw->iscsi_url->lun, task, data) == NULL) {
    PyErr_SetString(LibiscsiError, "Failed to send iSCSI CDB.");
    return NULL;
  }

  if (task->status == SCSI_STATUS_CHECK_CONDITION) {
    memcpy(sense_buf.buf, task->datain.data,
	   sense_buf.len < task->datain.size ?
	   sense_buf.len : task->datain.size);
    return Py_BuildValue("i", SCSI_STATUS_CHECK_CONDITION);
  }

  if (task->status == SCSI_STATUS_GOOD) {
    memcpy(datain_buf.buf, task->datain.data,
	   datain_buf.len < task->datain.size ?
	   datain_buf.len : task->datain.size);
    return Py_BuildValue("i", SCSI_STATUS_GOOD);
  }

  return Py_BuildValue("i", SCSI_STATUS_ERROR);
}

static PyObject *
libiscsi_close(PyObject *self, PyObject *args)
{
  unsigned long long tiw;
  struct iscsi_wrapper *iw;

  if (!PyArg_ParseTuple(args, "K", &tiw)) {
      PyErr_SetString(LibiscsiError, "Wrong number of arguments to libiscsi_close");
      return NULL;
  }

  iw = (struct iscsi_wrapper *)tiw;
  dl_iscsi_destroy_url(iw->iscsi_url);
  dl_iscsi_destroy_context(iw->iscsi);
  free(iw);
  return Py_BuildValue("i", 0);
}

static PyMethodDef LibiscsiMethods[] = {
    {"open",  libiscsi_open, METH_VARARGS, "Open an iSCSI device."},
    {"execute",  libiscsi_execute, METH_VARARGS, "Execute an iSCSI CDB."},
    {"close",  libiscsi_close, METH_VARARGS, "Close an iSCSI device."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initlibiscsi(void)
{
    PyObject *m;

    m = Py_InitModule("libiscsi", LibiscsiMethods);
    if (m == NULL)
        return;

    LibiscsiError = PyErr_NewException("libiscsi.error", NULL, NULL);
    Py_INCREF(LibiscsiError);
    PyModule_AddObject(m, "error", LibiscsiError);
}

static void __attribute__((constructor)) _init(void)
{
  libiscsi_handle = dlopen("libiscsi.so", RTLD_LAZY);
  if (libiscsi_handle == NULL) {
    fprintf(stderr, "Failed to dlopen(libiscsi): %s", dlerror());
    return;
  }

  dl_iscsi_create_context = dlsym(libiscsi_handle, "iscsi_create_context");
  if (dl_iscsi_create_context == NULL) {
    fprintf(stderr, "Failed to dlsym(iscsi_create_context): %s", dlerror());
  }
  dl_iscsi_destroy_context = dlsym(libiscsi_handle, "iscsi_destroy_context");
  if (dl_iscsi_destroy_context == NULL) {
    fprintf(stderr, "Failed to dlsym(iscsi_destroy_context): %s", dlerror());
  }
  dl_iscsi_get_error = dlsym(libiscsi_handle, "iscsi_get_error");
  if (dl_iscsi_get_error == NULL) {
    fprintf(stderr, "Failed to dlsym(iscsi_get_error): %s", dlerror());
  }
  dl_iscsi_parse_full_url = dlsym(libiscsi_handle, "iscsi_parse_full_url");
  if (dl_iscsi_parse_full_url == NULL) {
    fprintf(stderr, "Failed to dlsym(iscsi_parse_full_url): %s", dlerror());
  }
  dl_iscsi_destroy_url = dlsym(libiscsi_handle, "iscsi_destroy_url");
  if (dl_iscsi_destroy_url == NULL) {
    fprintf(stderr, "Failed to dlsym(iscsi_destroy_url): %s", dlerror());
  }
  dl_iscsi_set_targetname = dlsym(libiscsi_handle, "iscsi_set_targetname");
  if (dl_iscsi_set_targetname == NULL) {
    fprintf(stderr, "Failed to dlsym(iscsi_set_targetname): %s", dlerror());
  }
  dl_iscsi_set_session_type = dlsym(libiscsi_handle, "iscsi_set_session_type");
  if (dl_iscsi_set_session_type == NULL) {
    fprintf(stderr, "Failed to dlsym(iscsi_set_session_type): %s", dlerror());
  }
  dl_iscsi_set_header_digest = dlsym(libiscsi_handle, "iscsi_set_header_digest");
  if (dl_iscsi_set_header_digest == NULL) {
    fprintf(stderr, "Failed to dlsym(iscsi_set_header_digest): %s", dlerror());
  }
  dl_iscsi_full_connect_sync = dlsym(libiscsi_handle, "iscsi_full_connect_sync");
  if (dl_iscsi_full_connect_sync == NULL) {
    fprintf(stderr, "Failed to dlsym(iscsi_full_connect_sync): %s", dlerror());
  }

  dl_iscsi_scsi_command_sync = dlsym(libiscsi_handle, "iscsi_scsi_command_sync");
  if (dl_iscsi_scsi_command_sync == NULL) {
    fprintf(stderr, "Failed to dlsym(iscsi_scsi_command_sync): %s", dlerror());
  }
}

