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

#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <scsi/sg.h>

#include <Python.h>

#define SCSI_STATUS_GOOD            0
#define SCSI_STATUS_CHECK_CONDITION 2

#define SCSI_STATUS_SGIO_ERROR    0xff

static PyObject *SGIOError;

static PyObject *
sgio_open(PyObject *self, PyObject *args)
{
  const char *device;
  int readwrite;
  int s, v;

  if (!PyArg_ParseTuple(args, "si", &device, &readwrite))
    return NULL;

  readwrite = ((readwrite ? O_RDWR : O_RDONLY) | O_NONBLOCK);
  s = open(device, readwrite);
  if (s == -1) {
    PyErr_SetString(SGIOError, "Failed to open device.");
    return NULL;
  }

  if ((ioctl(s, SG_GET_VERSION_NUM, &v) < 0) || (v < 30000)) {
    PyErr_SetString(SGIOError, "Not an sg device, or old sg driver.");
    return NULL;
  }

  return Py_BuildValue("i", s);
}

static PyObject *
sgio_execute(PyObject *self, PyObject *args)
{
  PyObject *cdb_arg, *dataout_arg, *datain_arg, *sense_arg;
  Py_buffer cdb_buf, dataout_buf, datain_buf, sense_buf;
    sg_io_hdr_t io_hdr;
    int s;

    if (!PyArg_ParseTuple(args, "iOOOO:sgio_execute", &s,
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

    memset(&io_hdr, 0, sizeof(sg_io_hdr_t));
    io_hdr.interface_id = 'S';
    io_hdr.cmdp = cdb_buf.buf;
    io_hdr.cmd_len = cdb_buf.len;

    io_hdr.dxfer_direction = 0;
    if (dataout_buf.len) {
      io_hdr.dxfer_direction = SG_DXFER_TO_DEV;
      io_hdr.dxfer_len = dataout_buf.len;
      io_hdr.dxferp = dataout_buf.buf;
    }
    if (datain_buf.len) {
      io_hdr.dxfer_direction = SG_DXFER_FROM_DEV;
      io_hdr.dxfer_len = datain_buf.len;
      io_hdr.dxferp = datain_buf.buf;
    }

    io_hdr.sbp = sense_buf.buf;
    io_hdr.mx_sb_len = sense_buf.len;
    
    io_hdr.timeout = 20000;
    if (ioctl(s, SG_IO, &io_hdr) < 0) {
      PyErr_SetString(SGIOError, "SG_IO ioctl error.");
      return NULL;
    }

    if ((io_hdr.info & SG_INFO_OK_MASK) != SG_INFO_OK) {
        if (io_hdr.sb_len_wr > 0)
	        return Py_BuildValue("i", SCSI_STATUS_CHECK_CONDITION);

	    return Py_BuildValue("i", SCSI_STATUS_SGIO_ERROR);
   }

    return Py_BuildValue("i", SCSI_STATUS_GOOD);
}

static PyObject *
sgio_close(PyObject *self, PyObject *args)
{
  int s;

  if (!PyArg_ParseTuple(args, "i", &s)) {
      PyErr_SetString(SGIOError, "Wrong number of arguments to sgio_close");
      return NULL;
  }

  close(s);
  return Py_BuildValue("i", 0);
}

static PyMethodDef SGIOMethods[] = {
    {"open",  sgio_open, METH_VARARGS, "Open a SCSI device."},
    {"execute",  sgio_execute, METH_VARARGS, "Execute a SCSI CDB."},
    {"close",  sgio_close, METH_VARARGS, "Close a SCSI device."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initsgio(void)
{
    PyObject *m;

    m = Py_InitModule("sgio", SGIOMethods);
    if (m == NULL)
        return;

    SGIOError = PyErr_NewException("sgio.error", NULL, NULL);
    Py_INCREF(SGIOError);
    PyModule_AddObject(m, "error", SGIOError);
}
