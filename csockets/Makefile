# makefile for socket to work with pygame demo

CLIENT_SOURCES += receiver_client.cpp
SERVER_SOURCES += receiver_server.cpp

CC = g++

CFLAGS += -g -Wall -O0 -ggdb 

all: client server

client:
	$(CC) $(CFLAGS) $(CLIENT_SOURCES) -o client

server:
	$(CC) $(CFLAGS) $(SERVER_SOURCES) -o server

.PHONY: clean

clean:
	rm -f client server
