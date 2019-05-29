/**** SUBMITTING TO TEST PARSER FOR BASICS****/



#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "parse.h"

#define DELIMETERS " \"\n\t"

static char parsebuf[MAX_CMDLEN];

/* This buffer is declared as a translation unit static variable.  This
 * means that it will be allocated in the BSS (because it is
 * uninitialized), but that the symbol 'parsebuf' will not be visible in
 * any other translation units (that is, any other C files).  This
 * allows us to allocate exactly one buffer for reading and use it over
 * and over without having to malloc or use a large stack frame. */

char *ptrWords[MAX_WORDS];


/*
 * Parse a single line of input into words to be evaluated or executed
 * by the shell.  The value returned from this function is an array
 * allocated using malloc, pointing to strings also allocated using
 * malloc.  To indicate the end of the allocated array, its final entry
 * will be NULL.
 *
 * You may wish to change this structure substantially!
 */


char **parse_command() {

    if (fgets(parsebuf, sizeof(parsebuf), stdin) == NULL) {
        return NULL;
    }



    /* This is a non-parser!  You'll need to implement your parser here.
     * You don't have to use this function or this structure if you
     * prefer something different. */
    /* Read a single line from standard input, up to MAX_CMDLEN total
     * bytes including the terminating NUL. */


    char **oneWord;
    oneWord = malloc(2 * sizeof(char *));
    oneWord[0] = strdup(parsebuf);
    oneWord[1] = NULL;



    char **words = malloc(MAX_CMDLEN * sizeof(char *));
    char *word;

    word = strtok(oneWord[0], DELIMETERS);


    int i = 0;

    while (word != NULL) {

        words[i] = word;

        i++;

        word = strtok(NULL, DELIMETERS);
    }

    words[i] = NULL;


//    free(oneWord[0]);       // free up long single word
//    free(oneWord);

    return words;


}
