CFLAGS     = -O2
INCLUDE    = -I/usr/include
LIBS       = -L/usr/lib -liscsi
PYVER = 2.7

all: libiscsi_wrap.c

libiscsi_wrap.c: libiscsi.i
	@swig -python -shadow libiscsi.i

libiscsi_wrap.o: libiscsi_wrap.c
	${CC} -c ${CFLAGS} -fPIC ${INCLUDE} $$(python${PYVER}-config --cflags) libiscsi_wrap.c

clean:
	rm -f *.o *.so *.pyc *.c
