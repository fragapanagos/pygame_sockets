#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <unistd.h>
#include <cerrno>
#include <cstring>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>

// #include <arpa/inet.h>

#define PORT "50001" // the port client will be connecting to 

#define READSIZE 3 // max number of values to read in

using namespace std;

int main(int argc, char *argv[])
{
	int sockfd, numbytes;  
	double buf[READSIZE];
	struct addrinfo hints, *servinfo, *p;
	int rv;

	if (argc != 2) {
	    fprintf(stderr,"usage: client hostname\n");
	    exit(1);
	}

	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;

	if ((rv = getaddrinfo(argv[1], PORT, &hints, &servinfo)) != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
		return 1;
	}

	// loop through all the results and connect to the first we can
	for(p = servinfo; p != NULL; p = p->ai_next) {
		if ((sockfd = socket(p->ai_family, p->ai_socktype,
				p->ai_protocol)) == -1) {
			perror("client: socket");
			continue;
		}

		if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
			close(sockfd);
			perror("client: connect");
			continue;
		}

		break;
	}

	if (p == NULL) {
		fprintf(stderr, "client: failed to connect\n");
		return 2;
	}

	freeaddrinfo(servinfo); // all done with this structure

	while(1) {
		numbytes = recv(sockfd, buf, READSIZE * sizeof(double), 0);
		if (numbytes == -1) {
		    perror("recv");
		    exit(1);
		} else if (numbytes == 0) {
			cout << "controller closed, terminating receiver" << endl;
			break;
		}

		printf("Received (%f, %f, %f)\n", buf[0], buf[1], buf[2]);
	}

	close(sockfd);

	return 0;
}

