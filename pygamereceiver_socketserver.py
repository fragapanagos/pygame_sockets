import socket
import sys
from struct import unpack

# socket parameters
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50001              # Arbitrary non-privileged port

# create host socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();

# set socket to reuse socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind socket to address and port
try:
	s.bind((HOST, PORT))
except socket.error, msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Error message ' + msg[1]
	sys.exit()

s.listen(1) # only allow 1 connection in queue

# wait for client to connect
print 'waiting for client to connect'
conn, addr = s.accept()
s.close()
print 'Connected by', addr

done = False

while not done:
	# look for data in the socket
	data = conn.recv(1024)

	# run until we stop receiving data
	if not data:
		print 'controller closed, terminating receiver'
		done = True
	else:
		print 'Received', repr(unpack('ddd', data))

# close socket
conn.close()
