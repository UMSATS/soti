#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_INPUT_SIZE 64

int main()
{
    printf("Welcome to the SOTI CLI!\nOne day I'll put some ASCII art here like in the demo.\n\n");

    char recv_port[MAX_INPUT_SIZE];
    printf("Enter the port to receive messages from:\n");
    fgets(recv_port, MAX_INPUT_SIZE, stdin);
    // trims the newline character from the inputted device
    recv_port[strlen(recv_port) - 1] = '\0';

    // begin a listener thread to sniff telemetry messages
    printf("\nListening for telemetry messages…\n");
    pid_t listener_pid = fork();
    if(listener_pid == 0)
    {
        char* exec_args[] = {"python3", "listener.py", recv_port, NULL};
        execvp("python3", exec_args);
        exit(0);
    }

    char input[MAX_INPUT_SIZE];

    printf("\nAvailable commands:\nsend\nquery\nhelp\nexit\n"
        "Use \"-h\"/\"-help\" with any command for specifics.\n\n");

    while(1)
    {
        memset(input, '\0', MAX_INPUT_SIZE);
        printf("> ");
        fgets(input, MAX_INPUT_SIZE, stdin);

        if(!strcmp(input, "exit\n"))
        {
            kill(listener_pid, SIGTERM);
            printf("Exiting…\n");
            exit(0);
        }

        char* exec_args[] = {"python3", "cli.py", recv_port, input, NULL};
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