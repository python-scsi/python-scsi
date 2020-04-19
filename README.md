<!--
SPDX-FileCopyrightText: 2014 The python-scsi Authors

SPDX-License-Identifier: LGPL-2.1-or-later
-->

python-scsi
===========
python-scsi is a SCSI initiator for python.
It contains python classes to create and send SCSI commands to devices
accessible via:

* SGIO: /dev/sg* devices using ioctl(SG_IO)
  Depends on [cython-sgio](https://github.com/python-scsi/cython-sgio).

* iSCSI: iscsi://<server>/<iqn>/<lun>
  Depends on [cython-iscsi](https://github.com/python-scsi/cython-iscsi).

These classes also provide interfaces to marshall/unmarshall both CDBs
as well as DATA-IN/OUT buffers.


License
=======
Python-scsi is distributed under LGPLv2.1
Please see the LICENSE file for the full license text.


Getting the sources
===================
The module is hosted at https://github.com/python-scsi/python-scsi

You can use git to checkout the latest version of the source code using:

    $ git clone git@github.com:python-scsi/python-scsi.git

It is also available as a downloadable zip archive from:

    https://github.com/python-scsi/python-scsi/archive/master.zip


Building and installing
=======================

To build and install from the repository:

    python-scsi $ pip install .[iscsi,sgio]

You can avoid installing the optional dependencies by omitting the "extras":

    python-scsi $ pip install .

Tools (examples)
================
The tools directory contains example programs written against the python-scsi
API.

inquiry.py
----------
An example tool to send INQUIRY commands to a device.

mtx.py
------
An example tool to operate a SCSI media changer. Similar to, but not as
advanced as, the 'mtx' utility.


Mailinglist
===========
A mailinglist for python-scsi is available at:
https://groups.google.com/forum/#!forum/python-scsi
