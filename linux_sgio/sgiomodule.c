/* ========================================================================== **
 *                                sgiomodule.c
 *
 * Copyright:
 *  Copyright (C) 2014 by Ronnie Sahlberg <ronniesahlberg@gmail.com>
 *  Copyright (C) 2014 by Christopher R. Hertel <crh@ubiqx.org>
 *
 * Description: A Python binding for the Linux SCSI Generic (sg) Driver.
 *
 * -------------------------------------------------------------------------- **
 * License:
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU Lesser General Public License as published
 *  by the Free Software Foundation; either version 2.1 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public License
 *  along with this program; if not, see <http://www.gnu.org/licenses/>.
 *
 * -------------------------------------------------------------------------- **
 * References:
 *  + Linux SCSI Generic (sg) Driver: http://sg.danny.cz/sg/
 *  + Tour the Linux generic SCSI driver:
 *      http://www.ibm.com/developerworks/library/l-scsi-api/
 *  + Extending Python with C or C++:
 *      https://docs.python.org/2/extending/extending.html
 *  + Python Extension Programming with C:
 *      http://www.tutorialspoint.com/python/python_further_extensions.htm
 *
 * See Also:
 *  + The Linux SCSI Generic (sg) HOWTO:
 *      (Though out of date, this Linux 2.4 doc provides useful info.)
 *      http://www.tldp.org/HOWTO/SCSI-Generic-HOWTO/index.html
 *
 *
 * ========================================================================== **
 */

#include <stdio.h>      /* For snprintf(3).                       */
#include <errno.h>      /* For <errno>.  See errno(3).            */
#include <string.h>     /* For strerror(3).                       */
#include <stdarg.h>     /* For the <__VA_ARGS__> macro.           */
#include <fcntl.h>      /* Manipulate file descriptors; fcntl(2). */
#include <sys/ioctl.h>  /* I/O Control device; see ioctl(2).      */
#include <sys/stat.h>   /* File status information; see stat(2).  */
#include <sys/types.h>  /* System types; see types.h(0).          */
#include <scsi/sg.h>    /* sg driver header.  See references.     */

#include <Python.h>     /* Python extensions header.  See References. */


/* -------------------------------------------------------------------------- **
 * Defined constants:
 *
 *  bSIZE                       - Internal buffer size.  This *should be*
 *                                more than we'll ever need, but we always
 *                                check.  "In theory, theory and practice
 *                                are the same.  In practice, they're not."
 *                                See also: <bufr> & the <bufrstr()> macro.
 *
 * The SCSI_STATUS_* values are error codes that can be returned by the
 * <sgio_execute()> function.  Most are direct mappings from SCSI status
 * byte values, defined as part of the T-10 SCSI Architecture specification.
 * The exception is <SCSI_STATUS_SGIO_ERROR>, which is a catch-all for
 * "bad thing happened".
 * See:
 *  - http://en.wikipedia.org/wiki/SCSI_Status_Code
 *  - http://en.wikipedia.org/wiki/SCSI_check_condition
 *
 *  SCSI_STATUS_GOOD            - The command was successfully completed by
 *                                the target.
 *  SCSI_STATUS_CHECK_CONDITION - The target needs to report an error.  The
 *                                initiator should send a Request Sense
 *                                command to retrieve the error information.
 *  SCSI_STATUS_SGIO_ERROR      - An error occurred and was not handled by
 *                                this module.
 */

#define bSIZE 128

#define SCSI_STATUS_GOOD            0x00    /* Good.  */
#define SCSI_STATUS_CHECK_CONDITION 0x02    /* Bad.   */
#define SCSI_STATUS_SGIO_ERROR      0xff    /* Ugly.  */


/* -------------------------------------------------------------------------- **
 * Macros:
 *
 *  bufrstr() - Use the global <bufr> as scratch space to compose strings.
 *  ErrStr    - Shorthand for the error message associated with <errno>.
 */

#define bufrstr( ... ) (void)snprintf( bufr, bSIZE, __VA_ARGS__ )
#define ErrStr (strerror( errno ))


/* -------------------------------------------------------------------------- **
 * Global variables:
 *
 *  bufr      - String composition buffer.
 *  SGIOError - A PyObject that will be initialized in initsgio() as an
 *              Exception.  This is used to raise exceptions within the
 *              Python interpreter.
 */

char             bufr[bSIZE];
static PyObject *SGIOError;

/* -------------------------------------------------------------------------- **
 * Static functions:
 */

static PyObject *linux_sgio_open( PyObject *self, PyObject *args )
  /* ------------------------------------------------------------------------ **
   * Open a SCSI Generic I/O (SGIO) device.
   *
   *  Input:  self  - Always NULL.
   *                  For method calls, this would be the object itself.
   *                  For functions, this parameter is always NULL.
   *          args  - Function arguments, passed as a single PyObject.
   *
   *  Output: On success, the file descriptor of the opened device is
   *          returned.  On error, an exception is raised and NULL is
   *          returned (as specified in the Python docs).
   *
   *  Notes:  Something that always trips me up: "const char *" means that
   *          the pointer may be changed, but the character to which it
   *          points is immutable.
   *
   * ------------------------------------------------------------------------ **
   */
  {
  const char *device;       /* It's correct (const is so weird).    */
  int         readwrite;    /* Parsed PyObject; used as a boolean.  */
  int         fd;           /* File descriptor returned by open(2). */
  int         vers = 0;     /* Version number returned via ioctl(2).*/

  /* Grab the device pathname and value of <readwrite> from <args>.
   *  PyArg_ParseTuple() will raise an exception if the argument list
   *  cannot be parsed properly.
   */
  if( !PyArg_ParseTuple( args, "si", &device, &readwrite ) )
    return( NULL );

  /* Open the device. */
  readwrite = ((readwrite ? O_RDWR : O_RDONLY) | O_NONBLOCK);
  if( (fd = open( device, readwrite )) < 0 )
    {
    bufrstr( "Failed to open device %s; %s.", device, ErrStr );
    PyErr_SetString( SGIOError, bufr );
    return( NULL );
    }

  /* Make sure we can use the device we just opened.  */
  if( ioctl( fd, SG_GET_VERSION_NUM, &vers ) < 0 )
    {
    bufrstr( "%s is not an sg device.", device );
    PyErr_SetString( SGIOError, bufr );
    return( NULL );
    }
  if( vers < 30000 )
    {
    bufrstr( "Cannot use %s; Outdated sg driver.", device );
    PyErr_SetString( SGIOError, bufr );
    return( NULL );
    }

  /* Return the file descriptor as a Python integer.  */
  return( Py_BuildValue( "i", fd ) );
  } /* sgio_open */


static PyObject *linux_sgio_execute( PyObject *self, PyObject *args )
  /* ------------------------------------------------------------------------ **
   * Send a SCSI command to the target.
   *
   *  Input:  self  - Always NULL.
   *          args  - Function arguments, passed as a single PyObject.
   *
   *  Output: A status code, returned as an integer.  Possible values:
   *            0 - Success.
   *            2 - SCSI Check Condition.
   *          255 - SGIO Error.  See the SCSI Status byte in the returned
   *                message for specifics.
   *
   *  Notes:  CDB == Command Descriptor Block
   *          That is, basically, the message header.
   *
   * ------------------------------------------------------------------------ **
   */
  {
  PyObject   *cdb_arg, *dataout_arg, *datain_arg, *sense_arg;
  Py_buffer   cdb_buf,  dataout_buf,  datain_buf,  sense_buf;
  sg_io_hdr_t io_hdr;
  int         i;

  /* Parse and exctract the Python input parameters.
   *  See the discussion here:  https://docs.python.org/2/c-api/buffer.html
   */
  if( !PyArg_ParseTuple( args, "iOOOO:sgio_execute", &i,
                         &cdb_arg, &dataout_arg, &datain_arg, &sense_arg ) )
    return( NULL );
  if( PyObject_GetBuffer( cdb_arg, &cdb_buf, PyBUF_WRITABLE ) < 0 )
    return( NULL );

  if( PyObject_GetBuffer( dataout_arg, &dataout_buf, PyBUF_SIMPLE ) < 0 )
    return( NULL );

  /* We need either dataout or datain, we don't need both. */
  if ( dataout_buf.len <= 0 &&
       PyObject_GetBuffer( datain_arg, &datain_buf, PyBUF_WRITABLE ) < 0 )
    return( NULL );

  if( PyObject_GetBuffer( sense_arg, &sense_buf, PyBUF_WRITABLE ) < 0 )
    return( NULL );

  /* Prepare the sg device I/O header structure.  */
  memset( &io_hdr, 0, sizeof( sg_io_hdr_t ) );
  io_hdr.interface_id    = 'S';
  io_hdr.cmdp            = cdb_buf.buf;
  io_hdr.cmd_len         = cdb_buf.len;
  io_hdr.dxfer_direction = 0;

  if( dataout_buf.len )
    {
    io_hdr.dxfer_direction = SG_DXFER_TO_DEV;
    io_hdr.dxfer_len       = dataout_buf.len;
    io_hdr.dxferp          = dataout_buf.buf;
    }
  else if( datain_buf.len )
    {
    io_hdr.dxfer_direction = SG_DXFER_FROM_DEV;
    io_hdr.dxfer_len       = datain_buf.len;
    io_hdr.dxferp          = datain_buf.buf;
    }
  else
    {
    PyErr_SetString( SGIOError, "No input or output buffer provided." );
    return( NULL );
    }

  io_hdr.sbp       = sense_buf.buf;
  io_hdr.mx_sb_len = sense_buf.len;
  io_hdr.timeout   = 20000;

  /* Call ioctl(2).
   *  Raise a Python exception if the call fails.
   */
  if( ioctl( i, SG_IO, &io_hdr ) < 0 )
    {
    bufrstr( "SG_IO ioctl error; %s.", ErrStr );
    PyErr_SetString( SGIOError, bufr );
    return( NULL );
    }

  /* Check the status byte for a check condition or error.
   */
  if( ( io_hdr.info & SG_INFO_OK_MASK ) != SG_INFO_OK )
    {
    if( io_hdr.sb_len_wr > 0 )
      return( Py_BuildValue( "i", SCSI_STATUS_CHECK_CONDITION ) );
    else
      return( Py_BuildValue( "i", SCSI_STATUS_SGIO_ERROR ) );
    }

  /* All is well. */
  return( Py_BuildValue( "i", SCSI_STATUS_GOOD ) );
  } /* sgio_execute */


static PyObject *linux_sgio_close( PyObject *self, PyObject *args )
  /* ------------------------------------------------------------------------ **
   * Close a previously opened SGIO device.
   *
   *  Input:  self  - Always NULL.
   *          args  - Function arguments, passed as a single PyObject.
   *
   *  Output: NULL on error (and an SGIOError will be raised).
   *          On success, a PyObject containing integer value zero (0).
   *
   * ------------------------------------------------------------------------ **
   */
  {
  int fd;

  /* Extract the file descriptor from Python <args>.  */
  if( !PyArg_ParseTuple( args, "i", &fd ) )
    {
    PyErr_SetString( SGIOError, "Wrong number of arguments to sgio_close()." );
    return( NULL );
    }

  /* Attempt to close the file. */
  if( close( fd ) < 0 )
    {
    bufrstr( "Error on close(); %s.", ErrStr );
    PyErr_SetString( SGIOError, bufr );
    return( NULL );
    }

  /* Success. */
  return( Py_BuildValue( "i", 0 ) );
  } /* sgio_close */

/* We going to add some checking for Python 3 and additional code for the
 * 'new' way to define a module
 */

 static PyMethodDef SGIOMethods[] =
    {
      { "open",    linux_sgio_open,    METH_VARARGS, "Open a SCSI device."  },
      { "execute", linux_sgio_execute, METH_VARARGS, "Execute a SCSI CDB."  },
      { "close",   linux_sgio_close,   METH_VARARGS, "Close a SCSI device." },
      { NULL, NULL, 0, NULL }
    };

#if PY_MAJOR_VERSION >= 3

  static struct PyModuleDef moduledef =
    {
        PyModuleDef_HEAD_INIT,
        "linux_sgio",
        NULL,
	-1,
        SGIOMethods,
    };

  #define INITERROR return NULL

  PyObject *PyInit_linux_sgio(void)

#else

  #define INITERROR return

  void initlinux_sgio(void)

#endif
  /* ------------------------------------------------------------------------ **
   * Module initialization.
   * ------------------------------------------------------------------------ **
   */
  {
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("linux_sgio", SGIOMethods);
#endif
      if( module == NULL)
        INITERROR;

      SGIOError = PyErr_NewException( "linux_sgio.SGIOError", NULL, NULL );
      Py_INCREF(SGIOError);
      if ( PyModule_AddObject(module, "SGIOError", SGIOError) == -1 )
	INITERROR;

    if (SGIOError == NULL)
    {
        Py_DECREF(module);
        INITERROR;
    }
#if PY_MAJOR_VERSION >= 3
    return module;
#endif

  } /* initsgio */

/* ========================================================================== */
