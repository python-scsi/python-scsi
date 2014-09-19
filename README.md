# python-scsi


## What is it?

Python classes to access SG_IO scsi devices ...
It's not intended to be a wrapper for other tools, like sg3_utils, so the code is splitted in two main pieces. A Python C Extention, with basic functionality to do calls to ioctl, and a python package to utilize the the c extention methods. 

## How to build/install an run the code?

### get the source

You can either use git to clone the source or simple download the zip from:

https://github.com/rosjat/python-scsi/archive/master.zip 

Then unzip it to your filesystem (mainly somewere in your home directory).
If you use git simply use the following command in your shell:

    $ git clone git@github.com:rosjat/python-scsi.git
 
This will clone the source code to the current directory. If you download the zip archive with the source then you  just need to unpack on your machine.  

### build

You usally will use the setup.py script to build the package and therefore you can various options. The simplest way is just use the build option. If you are already in the source folder just use:

    $ python setup.py build
    
This will create a build folder in the actual folder with all the nessesary files. At this point you could simply install the packages. To get all options available for the setup script just check out the distutils package.

### install

After you have build the  package you can install it with pip:

    $ pip install .
    
this would install the package in the dist-package folder of your python distribution. It's recommended to use virtual environments. Since we don't write a "how to create a virtual environment" just use a search engine you like and look it up. 

### run

## How to use the code?


## TODO

 - write something usefull in the README section
 

## Be in the mix ...


Mailinglist: https://groups.google.com/forum/#!forum/python-scsi

