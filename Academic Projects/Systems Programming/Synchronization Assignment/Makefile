CC := gcc
CFLAGS := -g -O2 -Wall -Werror -pthread -std=c99 -D_DEFAULT_SOURCE
LDFLAGS := -pthread

TEST_SOURCES := binary_semaphore counting_semaphore synchronous_work
TEST_SOURCES += parallel_work

TESTS := $(patsubst %,test_%,$(TEST_SOURCES))

all:

test: $(TESTS)
	@for test in $(TESTS); do \
	    echo -n "$$test: "; \
	    ./$$test; \
	done; \
	exit 0

clean:
	rm -f *~ src/*~ src/*.o $(TESTS)

submission: submission.tar

submission.tar: Makefile src/csesem.c src/workqueue.c
	tar cf submission.tar $^

%.o: %.c
	$(CC) -c $< -o $@ $(CFLAGS)

test_%: tests/%.o src/csesem.o src/workqueue.o
	$(CC) -o $@ $^ $(LDFLAGS)

.PHONY: all clean test
