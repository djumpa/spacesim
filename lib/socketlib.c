#include "socketlib.h"

int init_socket_server(int *s,struct sockaddr_in *s_addr, int port, char *address )
{  
    int permission = 1;
    
    *s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP); /* open the socket */
    if (s < 0)
    {
        perror("socket");
        return 1;
    }

    /* get permission to broadcast */
    if (setsockopt(*s, SOL_SOCKET, SO_BROADCAST, &permission,
                   sizeof(permission)) < 0)
    {
        perror("permission");
        return 2;
    }
    printf("ready to write\n");
    s_addr->sin_addr.s_addr = inet_addr(address);
    s_addr->sin_family = AF_INET;
    s_addr->sin_port = htons(port);
    

    return 0;
}

int init_socket_client(int *s,struct sockaddr_in *s_addr, int port, char *address )
{     
    int permission = 1;

    s_addr->sin_family = AF_INET;
    s_addr->sin_addr.s_addr = htonl(INADDR_ANY);
    s_addr->sin_port = htons(port);
    
    *s = socket(AF_INET, SOCK_DGRAM, 0); /* open the socket */
    if (s < 0)
    {
        perror("socket");
        return 1;
    }
    /* get permission to read broadcast packets */
    if (setsockopt(*s, SOL_SOCKET, SO_BROADCAST, &permission,
                   sizeof(permission)) < 0)
    {
        perror("permission");
        return 2;
    }
    /* bind the socket to its structure */
    if (bind(*s, (struct sockaddr *)s_addr, sizeof(*s_addr)) < 0)
    {
        perror("bind");
        return 3;
    }
    printf("ready to read\n");

    return 0;
}