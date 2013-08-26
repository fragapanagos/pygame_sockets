import socket
import sys
from pygame_interface import PyGameController

# socket parameters
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50001              # Arbitrary non-privileged port

# create host socket
try:
	# IP4, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();

# set socket to reuse socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind socket to address and port
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

s.listen(1) # only allow 1 connection in queue

# wait for client to connect
print 'waiting for client to connect'
conn, addr = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])

# once we've created a connection socket from the server, we can close the server
s.close()

# create pygame user interface
controller = PyGameController()

# run controller
controller.run(conn)
