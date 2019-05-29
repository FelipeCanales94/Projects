CC := gcc
CFLAGS := -O2 -Wall -Werror -std=c99 -D_DEFAULT_SOURCE

# You should add source files to your shell by modifying the list of
# source files in the variable SOURCES.  This will automatically add
# dependencies to the build rule 'shell', so they will be compiled and
# linked with your shell.  It will also include those source files in
# the files submitted for grading.  You may use as many or as few source
# files as you like, but they should all appear in the src/
# subdirectory.
SOURCES := src/main.c src/parse.c

all: shell

# This causes your shell to depend on every .c file listed in $(SOURCES)
# transformed to a .o file.
shell: $(patsubst %.c,%.o,$(SOURCES))
	$(CC) -o shell $^

submission: submission.tar

submission.tar: Makefile $(SOURCES) src/*.h
	tar cf submission.tar $^

writeargs: tests/writeargs.o
	$(CC) -o writeargs $^

%.o: %.c
	$(CC) -c -o $@ $(CFLAGS) $<

clean:
	rm -f submission.tar shell writeargs
	rm -f *~ src/*~ tests/*~ src/*.o tests/*.o

.PHONY: all clean submission
