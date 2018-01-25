CFLAGS     = -O2
INCLUDE    = -I/usr/include
LIBS       = -L/usr/lib -liscsi
PYVER = 2.7

all: libiscsi_wrap.c

libiscsi_wrap.c: libiscsi.i
	@swig -python -shadow libiscsi.i
	rm -f libiscsi.py

clean:
	rm -f *.o *.so *.pyc *.c libiscsi.py
