/* program to read UDPs */
#include <unistd.h> // for close

#include "../lib/socketlib.h"

#define PORT_RECEIVE 92000
#define PORT_SEND 92001
#define DEFAULT_GROUP "127.0.0.1"

int main(int argc, char **argv)
{
    printf("Simulation program\n");
    int s, s_send;
    struct sockaddr_in s_addr, s_addr_send;
    int pktcount;
    int addr_len = sizeof(s_addr);

    int Buffer[2];
    Vector3f buffer_float[2];
    Vector3f pos = {0.0f, 0.0f, 0.0f};
    Vector3f vel = {0.0f, 0.0f, 0.0f};
    int retval;
    init_socket_server(&s_send, &s_addr_send, PORT_SEND, DEFAULT_GROUP);
    init_socket_client(&s, &s_addr, PORT_RECEIVE, DEFAULT_GROUP);

    float dt = 0.01f;

    while (1)
    {
        //send
        retval = sendto(s_send, &buffer_float, sizeof(buffer_float), 0, /* send the packet */
                        (struct sockaddr *)&s_addr_send, sizeof(s_addr_send));

        if (retval < 0)
        {
            perror("send");
            return 3;
        }

        if (pktcount >= 5000)
        {
            printf("S->FC\n");
            fflush(stdout);
        }

        //Actual logic
        vel.x = 1.0f;
        vel.y = 1.1f;
        vel.z = 0.9f;

        pos.x = pos.x + vel.x * dt;
        pos.y = pos.y + vel.y * dt;
        pos.z = pos.z + vel.z * dt;

        buffer_float[0] = pos;
        buffer_float[1] = vel;


        retval = recvfrom(s, Buffer, sizeof(Buffer), 0, /* get a packet */
                          (struct sockaddr *)&s_addr, &addr_len);
        if (retval < 0)
        {
            perror("recvfrom");
            return 4;
        }

        if (pktcount >= 5000)
        {
            printf("R0: %i\n", Buffer[0]);
            printf("R1: %i\n", Buffer[1]);
            fflush(stdout);
        }
        if (pktcount >= 5000)
            pktcount = 0;
        pktcount = pktcount + 1; /* log every 50th packet */
    }
    close(s); /* close the socket */
    return 0;
}