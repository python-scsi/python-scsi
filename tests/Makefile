CDB_TESTS = $(subst .py, , $(sort $(wildcard test_cdb_*.py)))
UNMARSHALL_TESTS = $(subst .py, , $(sort $(wildcard test_unmarshall_*.py)))
MISC_TESTS = test_enum test_opcode_mapper

all: misc_tests cdb_tests unmarshall_tests

cdb_tests: $(CDB_TESTS)

unmarshall_tests: $(UNMARSHALL_TESTS)

misc_tests: $(MISC_TESTS)

% :: %.py
	@echo "Running" $@
	@PYTHONPATH=.. python $<

