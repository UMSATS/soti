#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_INPUT_SIZE 64

int main()
{
    printf("Welcome to the SOTI CLI!\nOne day I'll put some ASCII art here like in the demo.\n"
        "Available commands:\nsend\nquery\nhelp\nexit\n"
        "Use \"-h\"/\"-help\" with any command for specifics.\n");

    char input[MAX_INPUT_SIZE];

    while(1)
    {
        memset(input, '\0', MAX_INPUT_SIZE);
        printf("> ");
        fgets(input, MAX_INPUT_SIZE, stdin);

        if(!strcmp(input, "exit\n"))
        {
            printf("Exiting…\n");
            exit(0);
        }

        char* exec_args[] = {"python3", "cli.py", input, NULL};
        pid_t new_pid = fork();
        if(new_pid == 0)
        {
            execvp("python3", exec_args);
            exit(0);
        }
        else
        {
            wait(&new_pid);
        }
    }
}