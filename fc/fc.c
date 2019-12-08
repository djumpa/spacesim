#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <termios.h>
#include <unistd.h> // for close
#define DEFAULT_PORT 12345
#define DEFAULT_GROUP "127.0.0.1"

int init_socket_server();

int main()
{
    printf("Flight Control program\n");
    init_socket_server();

    int Buffer[200];
    int port = DEFAULT_PORT;
    int retval;
    int fromlen;
    int pktcount = 0;
    int permission = 1;
    struct sockaddr_in s_addr;
    int s, addr_len;
    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP); /* open the socket */
    if (s < 0)
    {
        perror("socket");
        return 1;
    }

    /* get permission to broadcast */
    if (setsockopt(s, SOL_SOCKET, SO_BROADCAST, &permission,
                   sizeof(permission)) < 0)
    {
        perror("permission");
        return 2;
    }
    printf("ready to write\n");
    s_addr.sin_addr.s_addr = inet_addr(DEFAULT_GROUP);
    s_addr.sin_family = AF_INET;
    s_addr.sin_port = htons(DEFAULT_PORT);
    addr_len = sizeof(s_addr);

    //return 0;

    while (1)
    {
        Buffer[0] = 12345678; /* set arbitrary values in the buffer */
        Buffer[1] = 87654321;
        retval = sendto(s, &Buffer, sizeof(Buffer), 0, /* send the packet */

                        (struct sockaddr *)&s_addr, addr_len);

        if (retval < 0)
        {
            perror("send");
            return 3;
        }
        pktcount = pktcount + 1; /* log every 50th packet */
        if (pktcount >= 500)
        {
            pktcount = 0;
            printf(".");
            fflush(stdout);
        }


    }
    close(s); /* close the socket */
    return 0;
}

int init_socket_server()
{
}