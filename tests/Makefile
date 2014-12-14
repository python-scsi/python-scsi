CDB_TESTS = $(subst .py, , $(sort $(wildcard test_cdb_*.py)))
UNMARSHALL_TESTS = $(subst .py, , $(sort $(wildcard test_unmarshall_*.py)))

all: cdb_tests unmarshall_tests

cdb_tests: $(CDB_TESTS)

unmarshall_tests: $(UNMARSHALL_TESTS)

% :: %.py
	@echo "Running" $@
	@PYTHONPATH=.. python $<

