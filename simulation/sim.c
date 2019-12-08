/* program to read UDPs */
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <termios.h>
#include <unistd.h> // for close
#define DEFAULT_PORT 12345
#define DEFAULT_GROUP "127.0.0.1"
int main(int argc, char **argv)
{
    int Buffer[200];
    int port = DEFAULT_PORT;
    int retval;
    int fromlen;
    int pktcount;
    struct sockaddr_in s_addr;
    int s;
    int addr_len;
    int permission = 1;
    addr_len = sizeof(s_addr);
    s_addr.sin_family = AF_INET;
    s_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    s_addr.sin_port = htons(DEFAULT_PORT);
    s = socket(AF_INET, SOCK_DGRAM, 0); /* open the socket */
    if (s < 0)
    {
        perror("socket");
        return 1;
    }
    /* get permission to read broadcast packets */
    if (setsockopt(s, SOL_SOCKET, SO_BROADCAST, &permission,
                   sizeof(permission)) < 0)
    {
        perror("permission");
        return 2;
    }
    /* bind the socket to its structure */
    if (bind(s, (struct sockaddr *)&s_addr, sizeof(s_addr)) < 0)
    {
        perror("bind");
        return 3;
    }
    printf("ready to read\n");
    while (1)
    {
        retval = recvfrom(s, Buffer, sizeof(Buffer), 0, /* get a packet */
                          (struct sockaddr *)&s_addr, &addr_len);
        if (retval < 0)
        {
            perror("recvfrom");
            return 4;
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