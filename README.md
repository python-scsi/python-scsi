python-scsi
===========
python-scsi is a SCSI initiator for python.
It contains python classes to create and send SCSI commands to devices
accessible via:

* SGIO: /dev/sg* devices using ioctl(SG_IO)
  Only available for Linux

* iSCSI: iscsi://<server>/<iqn>/<lun>
  Available on all platforms which have libiscsi-python
  See https://github.com/sahlberg/libiscsi-python

These classes also provide interfaces to marshall/unmarshall both CDBs
as well as DATA-IN/OUT buffers.


License
=======
Python-scsi is distributed under LGPLv2.1
Please see the LICENSE file for the full license text.


Getting the sources
===================
The module is hosted at https://github.com/rosjat/python-scsi

You can use git to checkout the latest version of the source code using:

    $ git clone git@github.com:rosjat/python-scsi.git

It is also available as a downloadable zip archive from:

    https://github.com/rosjat/python-scsi/archive/master.zip 


Building and installing
=======================
Building the module:

    $ python setup.py build
    
Installing the module:

    $ python setup.py install


Unit testing
============
The tests directory contain unit tests for python-scsi.
To run the tests:

   $ cd tests
   $ make


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
