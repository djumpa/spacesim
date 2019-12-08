#include <stdio.h>
#include <unistd.h> // for close

#include "../lib/socketlib.h"

#define PORT_RECEIVE 92001
#define PORT_SEND 92000
#define DEFAULT_GROUP "127.0.0.1"

int main()
{
    printf("Flight Control program\n");
    int s, s_send;
    struct sockaddr_in s_addr, s_addr_send;
    init_socket_server(&s_send, &s_addr_send, PORT_SEND, DEFAULT_GROUP);
    init_socket_client(&s, &s_addr, PORT_RECEIVE, DEFAULT_GROUP);

    int Buffer[2];
    Vector3f buffer_float[2];
    int retval;
    int pktcount = 0;
    int addr_len = sizeof(s_addr);

    while (1)
    {
        retval = recvfrom(s, buffer_float, sizeof(buffer_float), 0, /* get a packet */
                          (struct sockaddr *)&s_addr, &addr_len);
        if (retval < 0)
        {
            perror("recvfrom");
            return 4;
        }

        if (pktcount >= 5000)
        {
            printf("pos: (%4.2f,%4.2f,%4.2f)\n", buffer_float[0].x, buffer_float[0].y, buffer_float[0].z);
            printf("vel: (%4.2f,%4.2f,%4.2f)\n", buffer_float[1].x, buffer_float[1].y, buffer_float[1].z);
            fflush(stdout);
        }

        Buffer[0] = 12345678; /* set arbitrary values in the buffer */
        Buffer[1] = 87654321;
        retval = sendto(s_send, &Buffer, sizeof(Buffer), 0, /* send the packet */
                        (struct sockaddr *)&s_addr_send, sizeof(s_addr_send));

        if (retval < 0)
        {
            perror("send");
            return 3;
        }

        if (pktcount >= 5000)
        {
            printf("FC->S\n");
            fflush(stdout);
        }

        if (pktcount >= 5000)
            pktcount = 0;
        pktcount = pktcount + 1; /* log every 50th packet */
    }
    close(s); /* close the socket */
    return 0;
}
