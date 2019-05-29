#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
/* The definitions for functions defined in parse.c are in parse.h */
#include "parse.h"
#include <ctype.h>



//TODO: FIGURE OUT HOW TO USE LESS MEMORY. TOO MUCH MEMORY IS BEING WASTED. #WHERE_IS_MY_GARBAGE_COLLECTOR
struct ShellVariables *list = NULL;


/* Function declarations for built in commands */
int builtinCd(char **args);

int builtinExport(char **args);

int builtinUnset(char **args);

int exiting(char **args);

//list to hold shell variables



/* Built - in Commands */
//TODO: FOR PART 2, CHANGE THIS TO A STRUCT
char *builtinCommands[] = {
        "cd",
        "export",
        "unset",
        "exit"
};

int (*builtin[])(char **) = {
        &builtinCd,
        &builtinExport,
        &builtinUnset,
        &exiting
};


//be able to add to list of shell variables
struct ShellVariables *append(struct ShellVariables *list, char *name, char *value) {

    struct ShellVariables *node = malloc(sizeof(struct ShellVariables));            //new node to add to list

    node->name = name;          // give new node specified data
    node->value = value;
    node->next = NULL;         // since append adds a new tail, next will always be NULL

    //if list empty, just make list the new node
    if (list == NULL) {
        list = node;
    } else {

        //find tail
        while (list->next != NULL) {
            list = list->next;
        }

        //make sure while loop did its job. if it did, make new node the tail
        if (list->next == NULL) {


            list->next = node;
        }

    }

    return list;

}

// remove shell variable from list
struct ShellVariables *list_remove(struct ShellVariables *list, char *name) {
    struct ShellVariables *temp;

    // 2 pointers to list head to keep track of nodes next to each other
    struct ShellVariables *temp2 = list;


    //Remove HEAD ---- NOTE: CANT REMOVE HEAD WITHOUT CREATING A NEW LIST SO JUST MODIFY THE DATA IN HEAD NODE/REST OF NODES AND DELETE THE TAIL
    if (strcmp(list->name, name) == 0) {
        temp = list;
        list = list->next;
        free(temp);


    } else { /* for all nodes excluding the head */

        temp = list;

        // find the node with that data
        while (strcmp(temp->name, name) != 0) {
            temp = temp->next;
        }
        //find node before the node with wanted data
        while (strcmp(temp2->next->name, temp->name) != 0) {
            temp2 = temp2->next;
        }

        //remove node with that data
        temp2->next = temp2->next->next;
        free(temp);

    }


    return list;
}

struct ShellVariables *list_find(struct ShellVariables *list, char *name) {
    /* Note that it is idiomatic in C to use for loops for non-numeric
     * iteration.  In this case, we assign the variable "cur" to the
     * head of a list, then iterate as long as we have not reached the
     * tail (cur == NULL, which means there are no more nodes).  The
     * iteration statement is to assign cur to the current node's next
     * pointer. */

    //loop thru list, if node with that data is found, return it. else return null
    for (struct ShellVariables *cur = list; cur != NULL; cur = cur->next) {
        if (strcmp(cur->name, name) == 0) {
            return cur;
        }
    }

    /* If we reach this point, we iterated the entire list without
     * finding a node containing the given data. */
    return NULL;
}


//checks for equal sign
int containsEqual(char **args) {

    int i = 0;

    while (args[0][i] != '\0') {
        if (args[0][i] == '=') {
            return 1;
        }
        i++;
    }

    return 0;
}

//get number of words
int getSize(char **args) {
    int i = 0;
    while (args[i] != NULL) {
        i++;
    }

    return i;
}

//checks whether we want to expand the variable or not
int containsDollarSign(char **args) {
    int i = 0;

    if (getSize(args) < 2) {
        return 0;
    }

    while (args[1][i] != '\0') {
        if (args[1][i] == '$') {
            return 1;
        }
        i++;
    }
    return 0;
}

int containsBackslash(char **args) {
    int i = 0;

    if (getSize(args) < 2) {
        return 0;
    }

    while (args[1][i] != '\0') {
        if (args[1][i] == '\\') {
            return 1;
        }
        i++;
    }

    return 0;
}


int containsDoubleQuotes(char **args) {
    int i = 0;

    if (getSize(args) < 2) {
        return 0;
    }

    while (args[1][i] != '\0') {
        if (args[1][i] == '\"') {
            return 1;
        }
        i++;
    }

    return 0;
}

int containsSingleQuotes(char **args) {
    int i = 0;

    if (getSize(args) < 2) {
        return 0;
    }

    while (args[1][i] != '\0') {
        if (args[1][i] == '\'') {
            return 1;
        }
        i++;
    }

    return 0;
}

int processes(char **args) {
    /*Same concept as lab we did*/
    pid_t parent;
    int checker;

    parent = fork();
    if (parent == 0) {
        if (execvp(args[0], args) == -1) {
            perror("exec");
        }
        exit(EXIT_FAILURE);
    } else if (parent < 0) {
        perror("exec");
    } else {
        do {

            waitpid(parent, &checker, WUNTRACED);
        } while (!WIFEXITED(checker) && !WIFSIGNALED(checker));
    }

    return 1;

}


int parsing(char **args) {



    // puts shell variable into shell list
    if (containsEqual(args) == 1) {

        int i = 0;
        int j = 0;
        int k = 0;
        char *name = malloc(1024);
        char *value = malloc(1024);

        while (args[0][i] != '=') {
            name[j] = args[0][i];
            j++;
            i++;
        }



        if (args[0][i] == '=') {
            i++;
        }

        while (args[0][i] != '\0') {
            value[k] = args[0][i];
            k++;
            i++;
        }


        if (list_find(list, name) == NULL) {
            list = append(list, name, value);
        } else {
            list_find(list, name)->value = value;
        }

        return 1;
    }

    if (containsDollarSign(args) == 1 && containsBackslash(args) != 1) {
        int i = 2;
        int j = 0;
        char *name = malloc(1024);
        while (args[1][i] != '}') {
            name[j] = args[1][i];
            j++;
            i++;
        }

        if (isEnviroVar(name) == 1) {
            args[1] = getenv(name);
            processes(args);
            //printf(getenv(name));
            return 1;
        } else if (isShellVar(name) == 1) {
            if (list_find(list, name)->value != NULL) {
                args[1] = list_find(list, name)->value;
                processes(args);
            }

        } else {
            args[1] = "";
            processes(args);
            return 1;
        }


        return 1;
    }


    if (containsBackslash(args) == 1) {
        int m = 0;
        int n = 0;      //fun fact, I used to love the letter n in middle school because Einstein used it...I realized I am no Einstein so I stopped using it

        char *temp = malloc(1028);
        while (args[1][n] != '\\') {
            temp[m] = args[1][n];
            m++;
            n++;
        }


        n++;

        while (args[1][n] != '\0') {
            temp[m] = args[1][n];
            m++;
            n++;
        }

        args[1] = temp;


        processes(args);

        return 1;


    }

    processes(args);


    return 1;
}

//check whether the variable is an environment variable or not
int isEnviroVar(char *args) {

    char *env = getenv(args);

    if (env == NULL || strlen(env) == 0) {
        return 0;
    }

    return 1;
}

int isShellVar(char *args) {
    int i = 0;
    for (struct ShellVariables *cur = list; cur != NULL; cur = cur->next, i++) {
        if (strcmp(cur->name, args) == 0) {
            return 1;
        }
    }

    return 0;
}


//TODO: Parse thru here. If argument is not a command, print to screen.
int doCommands(char **args) {


    if (args[0] == NULL) {
        return 1;
    }


    for (int i = 0; i < 4; i++) {
        //referenced from Piazza post by Vikram
        if (strcmp(args[0], builtinCommands[i]) == 0) {
            return (*builtin[i])(args);
        }
    }


    return parsing(args);
}


/* built-in cd */
int builtinCd(char **args) {
    //if there is no second argument

    if (args[1] == NULL) {
       if(chdir(getenv("HOME")) != 0){
           perror("exec");
       }
        // fprintf(stderr, "An argument to a directory was expected \n");
    } else {
        if (chdir(args[1]) != 0) {
            perror("exec");
        }
    }
    return 1;
}

/* quick exit by just typing exit */
int exiting(char **args) {
    exit(0);
    return 0;
}


/* built-in export */
int builtinExport(char **args) {
    char *name = malloc(1024);
    char *value = malloc(1024);

    int j = 0;
    int k = 0;
    int i = 0;

    if (list_find(list, args[1]) == NULL) {

        while (args[1][i] != '=') {

            name[j] = args[1][i];

            j++;
            i++;

        }

        if (args[1][i] == '=') {
            i++;
        }

        while (args[1][i] != '\0') {
            value[k] = args[1][i];
            k++;
            i++;
        }

        if (args[1] == NULL) {
            fprintf(stderr, "An argument to a create an enviroment variable was expected");
        } else {
            return setenv(name, value, 1);
        }
    } else {
        int hold = setenv(list_find(list, args[1])->name, list_find(list, args[1])->value, 1);
        list = list_remove(list, args[1]);
        return hold;
    }
    return -1;
}

/*built-in unset*/
int builtinUnset(char **args) {
    if (args[1] == NULL) {
        fprintf(stderr, "An argument to unset a variable was expected");
    } else {
        if (isEnviroVar(args[1]) == 1) {
            return unsetenv(args[1]);
        } else {
            if (isShellVar(args[1]) == 1) {
                list = list_remove(list, args[1]);
                return 0;
            }
        }

    }
    return -1;
}

/* Print a prompt if commands are coming from a user on the terminal. */
static void prompt() {
    /* The isatty (manual section 3) function tests whether a given file
     * descriptor is attached to a terminal, and returns true if it is.
     * This allows us to print a prompt only if there's an actual human
     * being sitting at the terminal.  If stdin is from a file, pipe, or
     * other redirection, the prompt will be suppressed. */

    char *flip = "PS1";

    if(list_find(list, flip) != NULL){
        fputs(list_find(list, flip)->value, stdout);
        fflush(stdout);
    } else if (isatty(STDIN_FILENO)) {
        fputs("$ ", stdout);
        fflush(stdout);
    }

}

int main(int argc, char *argv[]) {
    char **args;

    while (!feof(stdin) && !ferror(stdin)) {
        /* Print the prompt if we're on a terminal */
        prompt();
        /* Parse a single line of input into words */
        args = parse_command();
        if (args == NULL) {
            /* This probably indicates end of input */
            return 0;
        }

        /* This is probably where you'll implement shell builtin
         * handling, variable assignments, etc. You may want to write
         * helper functions that appear in this or other files for that
         * purpose.
         *
         * The default implementation just echoes the command that the
         * user typed with no changes. */


        doCommands(args);

    }






    /* If there was no error, return success. */
    return ferror(stdin);
}
