#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define BREAKPOINT 0x00000000004004f4
#define ADDR 0x610c

int main(int argc, char **argv) {
    // execv() needs a NULL-terminated array, so we copy from argv into
    // child_argv.
    char **child_argv  = calloc(argc, sizeof(char));
    int i;
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
        if (ptrace(PTRACE_TRACEME, 0, NULL, 0) == -1) {
            printf("ptrace: error %d", errno);
            return -1;
        }
        if (execv(argv[1], child_argv) == -1) {
            printf("execv: error %d", errno);
            return -1;
        }
    }

    // will be parent here!
    printf("we are in control!\n");
    ptrace(PTRACE_SETOPTIONS, child_pid, NULL,
           PTRACE_O_TRACEEXEC);
    sleep(2);

    ptrace(PTRACE_CONT, child_pid, NULL, 0);

    return 0;
}
