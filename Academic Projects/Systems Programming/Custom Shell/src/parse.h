#ifndef PARSE_H_
#define PARSE_H_

/* You are not required to handle any command longer than 1024 bytes
 * including the newline and terminating NUL byte.  If you read a longer
 * command line, you may assume that it was only 1023 bytes long and
 * proceed accordingly. */
#define MAX_CMDLEN 1024
#define MAX_WORDS 128

char **parse_command();
int isEnviroVar(char *args);
int isShellVar(char *args);
int containsDoubleQuotes( char **args);



struct ShellVariables {
    char *name;
    char *value;
    struct ShellVariables *next;
};

#endif /* PARSE_H_ */
