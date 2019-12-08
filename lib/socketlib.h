#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>

typedef struct Vector3f
{
    float x;
    float y;
    float z;
} Vector3f;


int init_socket_server(int *s, struct sockaddr_in *s_addr, int port, char *address);

int init_socket_client(int *s, struct sockaddr_in *s_addr, int port, char *address);