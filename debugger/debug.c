#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <unistd.h>

int main(int argc, char **argv) {
    // execvp() needs a NULL-terminated array, so we copy from argv into
    // child_argv.
    printf("parent pid: %d\n", getpid());
    char **child_argv  = calloc(argc - 1, sizeof(char));
    int i;
    printf("argc: %d\n", argc);
    for(i = 0; i < argc - 1; ++i) {
        child_argv[i] = argv[i+1];
    }

    if (argc < 2) {
        return -1;
    }
    pid_t child_pid = fork();
    if (child_pid == -1) { //error
        return -1;
    }

    if (child_pid == 0) { // child
        printf("child pid: %d\n", getpid());
        printf("argv[1]: %s\n", argv[1]);
        printf("child_argv[0]: %s\n", child_argv[0]);
        printf("child_argv[1]: %p\n", child_argv[1]);
        if (execv(argv[1], child_argv) == -1) {
            printf("oh noes, error %d has occurred!\n", errno);
            return -1;
        }
    }

    // will be parent here!
    printf("hi, I am %d and I have a child called %d!\n",
           getpid(), child_pid);
    return 0;
}
